@echo off
set PYTHONUTF8=1
echo Running Summary Script...
python d:\Panaverse\projects\hackathon_panaverse\scripts\send_summary.py > d:\Panaverse\projects\hackathon_panaverse\summary_output.log 2>&1
echo Done.
