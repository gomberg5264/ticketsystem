# Use nixos image with Python 3.11
FROM nixos/nix

# Set Nix channel to a valid stable version (let's use nixpkgs-unstable or nixpkgs-23.05 for example)
RUN nix-channel --add https://nixos.org/channels/nixpkgs-23.05 nixpkgs && \
    nix-channel --update

# Install Python 3.11
RUN nix-env -iA nixpkgs.python311

# Copy application code to the container
WORKDIR /app
COPY . /app

# Install any additional Python dependencies (if you have a requirements.txt file)
# Uncomment the following lines if you need to install dependencies:
# COPY requirements.txt /app/requirements.txt
# RUN python3.11 -m pip install -r requirements.txt

# Expose the local and external ports
EXPOSE 5000
EXPOSE 80

# Command to run the Flask app on port 5000
CMD ["python3.11", "app.py"]
