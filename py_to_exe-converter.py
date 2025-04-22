import os
import subprocess

def make_exe_from_all_py():
    current_dir = os.getcwd()
    py_files = [f for f in os.listdir(current_dir) if f.endswith(".py")]

    if not py_files:
        print("⚠️ इस फोल्डर में कोई .py फाइल नहीं मिली!")
        return

    for py_file in py_files:
        print(f"🚀 .exe बना रहे हैं: {py_file}")
        command = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            py_file
        ]
        subprocess.run(command)

    print("\n🎉 Done! सभी .exe फाइलें 'dist' फोल्डर में मिलेंगी।")

# चलाएं
make_exe_from_all_py()
