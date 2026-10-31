# Anaconda Setup on Amazon Linux EC2

Quick setup guide for installing Anaconda and Python on an Amazon Linux EC2 instance.

## Prerequisites
- Amazon Linux EC2 instance
- SSH access with key pair

## Connecting to EC2 Instance

Connect to your EC2 instance using SSH:

**From Windows (Command Prompt/PowerShell):**
```bash
# If pem file is in current directory
ssh -i "mcp.pem" ec2-user@<EC2_PUBLIC_DNS>

# If pem file is in .ssh folder
ssh -i "~/.ssh/mcp.pem" ec2-user@<EC2_PUBLIC_DNS>
```

**Note:** Always use `ec2-user` (not `root`) for Amazon Linux instances. The system will display a Deep Learning AMI welcome message showing available tools and GPU configurations.

## Installation Steps

1. **Update the system**
   ```bash
   sudo yum update -y
   ```

2. **Download Anaconda installer**
   ```bash
   curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh
   ```

3. **Run the installer**
   ```bash
   bash Anaconda3-2025.06-0-Linux-x86_64.sh
   ```
   - Follow the prompts
   - Accept the license agreement
   - Choose installation location: `~/anaconda3` (when prompted)
   - When asked about shell initialization, choose "no" initially

4. **Add Anaconda to PATH**
   ```bash
   export PATH="$HOME/anaconda3/bin:$PATH"
   echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

5. **Initialize conda**
   ```bash
   conda init bash
   source ~/.bashrc
   ```

## Verification

Check installations:
```bash
conda --version
python --version
pip --version
```

## Optional: Install uv (fast Python package manager)
```bash
pip install uv
```

You should now have a fully functional Anaconda environment with Python 3.13 and conda package manager.
## Run the server safely

`server.py` has no authentication, so anyone who can reach port 8000 can call its tools. It listens on `127.0.0.1` unless you set `MCP_HOST`.

```bash
# Before exposing it, limit the instance's security group to your own IP address on port 8000.
MCP_HOST=0.0.0.0 python server.py
```

`mcp-remote --allow-http` in `claude_desktop_config.json` sends traffic in plain text. Use it only for a short test from your own IP address, and put the server behind HTTPS and authentication before you share it.
