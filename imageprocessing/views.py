import os
import uuid
import subprocess
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404


def compress_pdf(input_path, output_path, target_size_mb=2.0):
    """
    Compress PDF using Ghostscript with multiple quality presets.
    Returns compressed file size in MB.
    """
    presets = ["/screen", "/ebook", "/printer"]  # from lowest to higher quality
    gs_executable = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"
    for preset in presets:
        gs_command = [
            gs_executable,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/screen",  # Low quality, max compression
            "-dDownsampleColorImages=true",
            "-dColorImageDownsampleType=/Average",
            "-dColorImageResolution=72",
            "-dDownsampleGrayImages=true",
            "-dGrayImageDownsampleType=/Average",
            "-dGrayImageResolution=72",
            "-dDownsampleMonoImages=true",
            "-dMonoImageDownsampleType=/Subsample",
            "-dMonoImageResolution=72",
            "-dCompressFonts=true",
            "-dEmbedAllFonts=true",
            "-dSubsetFonts=true",
            "-dAutoRotatePages=/None",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path,
        ]
        try:
            subprocess.run(gs_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ghostscript error: {e}")
            raise RuntimeError("PDF compression failed")

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Preset {preset} produced size: {size_mb:.2f} MB")

        if size_mb <= target_size_mb:
            return round(size_mb, 2)

    # If none of the presets achieve target size, return last size anyway
    return round(size_mb, 2)


def upload_and_compress_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        uploaded_file = request.FILES["pdf_file"]
        target_size = float(request.POST.get("target_size", 2.0))

        # Create unique filename to avoid overwrites
        unique_prefix = uuid.uuid4().hex
        safe_filename = f"{unique_prefix}_{uploaded_file.name}"

        # Save original uploaded PDF
        input_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(input_dir, exist_ok=True)
        input_path = os.path.join(input_dir, safe_filename)
        with open(input_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Prepare output directory and filename
        output_dir = os.path.join(settings.MEDIA_ROOT, "compressed")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f"compressed_{safe_filename}"
        output_path = os.path.join(output_dir, output_filename)

        # Compress PDF
        try:
            final_size = compress_pdf(input_path, output_path, target_size)
        except Exception as e:
            context = {"error": f"Compression failed: {str(e)}"}
            return render(request, "imageprocessing/compress_pdf.html", context)

        context = {
            "result": {
                "original_size": round(os.path.getsize(input_path) / (1024 * 1024), 2),
                "target_size": target_size,
                "final_size": final_size,
                "filename": output_filename,
            }
        }
        return render(request, "imageprocessing/compress_pdf.html", context)

    return render(request, "imageprocessing/compress_pdf.html")


def download_compressed_pdf(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "compressed", filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
    else:
        raise Http404("File not found")
    

from diffusers import StableDiffusionPipeline
import torch
import os
from uuid import uuid4
from django.conf import settings
from django.shortcuts import render

# Load Stable Diffusion model in CPU
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    use_auth_token=True  # You must get one from huggingface.co
)
pipe = pipe.to("cpu")  # <-- Fix here

def generate_local_ai_image(request):
    prompt = request.GET.get('prompt', 'A beautiful Indian village with 5G tower and kids using tablets')

    try:
        image = pipe(prompt).images[0]

        filename = f"{uuid4().hex}.png"
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        image.save(image_path)

        return render(request, 'imageprocessing/show_image.html', {
            'prompt': prompt,
            'image_url': settings.MEDIA_URL + filename
        })

    except Exception as e:
        return render(request, 'imageprocessing/show_image.html', {
            'prompt': prompt,
            'error': f"Image generation failed: {str(e)}"
        })
