# Compatibility entry point for the native Gmsh cavity-aware batch adapter.
$taskDriver = Join-Path $PSScriptRoot "gmsh_clamp_delaunay.py"
& python $taskDriver @args
exit $LASTEXITCODE
