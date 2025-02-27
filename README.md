# MediaPipe Hand Gesture Recognition

## Requirements
- Raspberry Pi 4 / 5 or Windows laptop/PC
- MIPI camera or USB webcam
- Operating system:
  - Rasbian Bookworm
  - Windows 10 and above

## Steps to Install & Run

### Installation Steps for Raspberry Pi 4 / 5

Before proceeding, verify that your Raspberry Pi has Python 3 installed by running:

```sh
python --version
```

Expected output:
```
Python 3.11.2 or Python 3.x.x
```

If Python is not installed, install it using:

```sh
sudo apt-get install python3
```

#### Step 1: Install Git
```sh
sudo apt-get install git
```

#### Step 2: Clone the Repository
```sh
git clone https://github.com/Deepanys/Mediapipe_handgesture.git
```

#### Step 3: Navigate to the Project Directory
```sh
cd Mediapipe_handgesture
```

#### Step 4: Create a Virtual Environment
```sh
python -m venv MediaPipe
```

#### Step 5: Activate the Virtual Environment
```sh
source MediaPipe/bin/activate
```

#### Step 6: Install Required Dependencies
```sh
pip install -r requirements.txt
```

---

## Running the Face and Hand Detection Script on Raspberry Pi

#### Step 1: Navigate to the Project Directory
```sh
cd Mediapipe_handgesture
```

#### Step 2: Activate the Virtual Environment
```sh
source MediaPipe/bin/activate
```

#### Step 3: Run the Script
```sh
python TrackFace_findGesture.py
```

---

## Installation Steps for Windows

Before proceeding, verify that Python 3 is installed by running:

```powershell
python --version
```

Expected output:
```
Python 3.11.2 or Python 3.x.x
```

If Python is not installed, download and install it from "Windows Store" or [Python Official Website](https://www.python.org/downloads/). Ensure you check the option to add Python to PATH during installation.

#### Step 1: Install Git
Download and install Git from [Git for Windows](https://git-scm.com/download/win).

#### Step 2: Clone the Repository
```powershell
git clone https://github.com/Deepanys/Mediapipe_handgesture.git
```

#### Step 3: Navigate to the Project Directory
```powershell
cd Mediapipe_handgesture
```

#### Step 4: Create a Virtual Environment
```powershell
python -m venv MediaPipe
```

#### Step 5: Activate the Virtual Environment
```powershell
MediaPipe\Scripts\activate
```

#### Step 6: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

---

## Running the Face and Hand Detection Script on Windows

#### Step 1: Navigate to the Project Directory
```powershell
cd Mediapipe_handgesture
```

#### Step 2: Activate the Virtual Environment
```powershell
MediaPipe\Scripts\activate
```

#### Step 3: Run the Script
```powershell
python TrackFace_findGesture.py
```

