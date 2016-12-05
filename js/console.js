var selector = 'a.J-media-item';/*<a href="/video/2678" class="J-media-item">*/
var videoes = [];/*包含name和url属性的视频对象组成的数组*/
var total = $(selector).length;/*教程下所有超链接的长度*/
$(selector).each(function(index,ele) {
    var href = this.href;
    var video_id = href.substring(href.lastIndexOf('/') + 1, href.length); // this.href.replace('http://www.imooc.com/video/', '');
    var video_name = this.innerText;//Node.innerText is a nonstandard property-->$(this).text()
    var time_pattern = /\(\d{2}:\d{2}\)/;//(03:25)
    if (!time_pattern.test(video_name)) {//true if there is a match between the regular expression and the specified string; otherwise, false.
       	total--;
        if (index == $(selector).length - 1 && !total) {
            console.log('没有视频可以下载！');
        }
        return;
    }
    video_name = video_name.replace(/\(\d{2}:\d{2}\)/, '').replace(/\s/g, '');//去掉时间，去掉空格，只留视频名称
    $.getJSON("/course/ajaxmediainfo/?mid=" + video_id + "&mode=flash", function(data) {
        var video_url = data.data.result.mpath[2];//高清视频地址
        videoes.push({
            file_index:index,/*这个属性用于验证push到videoes数组的元素并不按顺序*/
            file_name: video_name,
            file_url: video_url
        });
        if (videoes.length == total) {
        	console.log($('.hd .l').text());/*<div class="hd clearfix"><h2 class="l">AngularJS实战</h2>*/
            console.log('共' + total + '个视频。');
            //console.log(JSON.stringify(videoes));
            $(videoes).each(function(index,ele){
                console.log(JSON.stringify(ele)+'\n');
            })
         }
     });
});