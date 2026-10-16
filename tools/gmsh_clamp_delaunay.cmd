@echo off
python "%~dp0gmsh_clamp_delaunay.py" %*
exit /b %errorlevel%
