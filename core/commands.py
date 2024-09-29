import subprocess

script = "ImgGallery/core/download.sh"

# Execute the command
result = subprocess.run(["bash", script], capture_output=True, text=True)

# Print the output and error (if any)
print("Output:", result.stdout)
print("Error:", result.stderr)