$(document).ready(function() {
	var percent = 0, bar = $('.transition-timer-carousel-progress-bar'), crsl = $('#carouselHome');
    function progressBarCarousel() {
      bar.css({width:percent+'%'});
     percent = percent +0.5;
      if (percent>100) {
          percent=0;
          crsl.carousel('next');
      }      
    }
    crsl.carousel({
        interval: false,
        pause: true
    }).on('slide.bs.carousel', function () {percent=0;});var barInterval = setInterval(progressBarCarousel, 30);
    crsl.hover(
        function(){
            clearInterval(barInterval);
        },
        function(){
            barInterval = setInterval(progressBarCarousel, 30);
        })


//carousel animation fix
function animateElement(obj, anim_) {
    obj.addClass(anim_ + ' animated').one(
        'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
        function() {
            $(this).removeClass();
        });
}
$('#carouselHome, #carouselSubnav').on('slide.bs.carousel', function(e) {
    var current = $('.item').eq(parseInt($(e.relatedTarget).index()));
    $('[data-animation]').removeClass();
    $('[data-animation]', current).each(function() {
        var $this = $(this);
        var anim_ = $this.data('animation');
        animateElement($this, anim_);
    });
});
});
