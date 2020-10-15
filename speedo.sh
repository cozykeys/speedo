#!/usr/bin/env bash

action="$1"

speedo_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# TODO: Is there a better way? Submodule perhaps?
kbutil_dir="$( dirname "$speedo_dir" )/resources/kbutil"

kbutil_dll="$kbutil_dir/build/KbUtil.Console/bin/Release/kbutil.dll"
kbmath_dll="$kbutil_dir/build/KbMath.Console/bin/Release/KbMath.Console.dll"

svg_opener="inkscape"

function error() {
    local msg="$1"

    local COLOR_NONE='\033[0m'
    local COLOR_ERROR='\033[0;31m'

	>&2 echo -e "${COLOR_ERROR}ERROR: $msg${COLOR_NONE}"
    exit 1
}

function generate_render() {
    input="$speedo_dir/speedo.xml"
    output="$speedo_dir/case"

    options="--visual-switch-cutouts --keycap-overlays --keycap-legends --squash"

    mkdir -p "./temp"

    dotnet "$kbutil_dll" gen-svg $options "$input" "$output"
    dotnet "$kbutil_dll" gen-key-bearings "$input" "./temp/keys.json" --debug-svg="./temp/bearings.svg"

    "$svg_opener" "$output/speedo.svg"
}

function generate_case() {
    input="$speedo_dir/speedo.xml"
    output="$speedo_dir/case"

    options="--visual-switch-cutouts"

    mkdir -p "./temp"

    dotnet "$kbutil_dll" gen-svg $options "$input" "$output"
    dotnet "$kbutil_dll" gen-key-bearings "$input" "./temp/keys.json" --debug-svg="./temp/bearings.svg"

    "$svg_opener" $output/speedo_*.svg
}

function generate_layouts() {
    options="--visual-switch-cutouts --keycap-overlays --keycap-legends"

    dotnet "$kbutil_dll" gen-svg $options \
        "$speedo_dir/layout/speedo_layout.xml" \
        "$speedo_dir/layout"

    "$svg_opener" \
        "$speedo_dir/layout/speedo_layer_default.svg" \
        "$speedo_dir/layout/speedo_layer_fn.svg"
}

function print_usage() {
    echo "USAGE: ./speedo.sh <action> [OPTIONS]"
    echo ""
    echo "Actions:"
    echo "    generate-render       : Generate an svg render of the keyboard"
    echo "    generate-case         : Generate svg renders of the keyboard case layers"
    echo "    help                  : Print this help dialog"
}

if [ "$action" = "generate-render" ]; then
    generate_render
elif [ "$action" = "generate-case" ]; then
    generate_case
elif [ "$action" = "generate-layouts" ]; then
    generate_layouts
elif [ "$action" = "help" ]; then
    print_usage
else
    print_usage
    exit 1
fi
