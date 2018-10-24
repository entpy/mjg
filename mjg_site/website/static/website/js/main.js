$(document).ready(function () {
	var percent = 0, bar = $('.transition-timer-carousel-progress-bar'), crsl = $('#carouselHome');
	var timing = 10;
	crsl.carousel({ interval: false, pause: true }).on('slide.bs.carousel', function () { percent = 0; });
	function progressBarCarousel() {
		bar.css({
			width: percent + '%'
		});
		percent = percent + 0.1;
		if (percent > 100) {
			percent = 0;
			crsl.carousel('next');
		}
	}
	//carousel animation fix
	function animateElement(obj, anim_) {
		obj.addClass(anim_ + ' animated').one(
			'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
			function () {
				$(this).removeClass();
			});
	}
	var barInterval = setInterval(progressBarCarousel, timing);
	crsl.hover(
		function () {
			clearInterval(barInterval);
		},
		function () {
			barInterval = setInterval(progressBarCarousel, timing);
		})

	$('#carouselHome, #carouselSubnav').on('slide.bs.carousel', function (e) {
		var current = $('.item').eq(parseInt($(e.relatedTarget).index()));
		$('[data-animation]').removeClass();
		$('[data-animation]', current).each(function () {
			var $this = $(this);
			var anim_ = $this.data('animation');
			animateElement($this, anim_);
		});
	});

	/* services pie */
	$(document).on("click mouseover", ".servicePieAction", function(){
		var pieName = $(this).data("pieName");	

		// show selected text
		$(".servicePieContentAction").html($(".service_content_" + pieName).html());

		// show selected title
		$(".servicePieTitleAction").html($(".service_title_" + pieName).html());

		// set active only selected element on services pie
		$(".servicePieAction").removeClass("active");

		$(this).addClass("active");

		return false;
	});
});
