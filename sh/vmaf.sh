echo "==============="
echo "reference: $1"
echo "distorted: $2"
ffmpeg -hide_banner \
    -r 24 -i $(pwd)/$1 \
    -r 24 -i $(pwd)/$2 \
    -lavfi "[0:v]setpts=PTS-STARTPTS[reference]; \
            [1:v]setpts=PTS-STARTPTS[distorted]; \
            [distorted][reference]libvmaf=log_fmt=xml:log_path=/dev/null:model_path=/home/child2/vmaf/model/vmaf_float_v0.6.1.pkl:n_subsample=15:n_threads=2" \
    -f null -
echo "=============="
