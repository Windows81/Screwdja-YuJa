Param(
	[bool]$play = 0, [int]$incr = 1, [int]$ss = $incr + ((gc yuja.csv -tail 2 -Delimiter "`r")[0] -replace "^\s*(\d+)[^\0]+", "`$1"), [int]$stop = $ss - $incr)

for ($n = $ss; $n -ne $stop; $n += $incr) {
	$c = (iwr "https://uci.yuja.com/V/Video?v=$n").content;
	$t = [System.Web.HttpUtility]::HtmlDecode([regex]::Match($c, "<meta property=`"og:title`" content=`"(.+)`" />").Groups[1]) -replace '"', '""';
	$p = [regex]::Match($c, "https://uci.yuja.com/P/DataPage/BroadcastsThumb/\d+").value;
	if ($p) {
		$v = [regex]::Match((iwr $p -Method Head -MaximumRedirection 0 -SkipHttpErrorCheck -ErrorAction SilentlyContinue ).headers.location, 'Video-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}').value;
		if ($v) {
			$l = "https://coursecast-chatter.s3.us-west-2.amazonaws.com/$($v)_processed.mp4";
			echo $n $l $t "";
			ac yuja.csv "$n,`"$t`",`"$l`",";
			if ($play) { start "C:\Program Files\VideoLAN\VLC\vlc.exe" $l -Wait }
		}
	}
}