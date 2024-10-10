proc draw_dashed_line {x1 y1 z1 x2 y2 z2 num_segments color_name} {
    set dx [expr {($x2 - $x1) / $num_segments}]
    set dy [expr {($y2 - $y1) / $num_segments}]
    set dz [expr {($z2 - $z1) / $num_segments}]

    for {set i 0} {$i < $num_segments} {incr i 2} {
        set start [list [expr {$x1 + $i * $dx}] [expr {$y1 + $i * $dy}] [expr {$z1 + $i * $dz}]]
        set end [list [expr {$x1 + ($i + 1) * $dx}] [expr {$y1 + ($i + 1) * $dy}] [expr {$z1 + ($i + 1) * $dz}]]

        graphics top color $color_name
        graphics top cylinder $start $end radius 0.1
    }
}