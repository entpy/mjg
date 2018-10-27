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

	lawCookieCompliance.createDivOnLoad();

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

function page_anchor(anchorName) {
	if (!anchorName) {
		var window_location = window.location;
		var myRe = new RegExp("#(.+)$");
		var myArray = myRe.exec(window_location);
	}

	if (myArray) {
		var scrollToElement = myArray[1];
	} else if (anchorName) {
		var scrollToElement = anchorName;
	}

	$.scrollTo('#_' + scrollToElement, 2500, { offset:-80 });

	return true;
}

// TODO
// Validazione form
// inserirlo in unn oggetto
function validateForm(constraints) {
	// elimino eventuali classi di errore
	clearFormErrorClasses();

	// lavora sui "name" NON sugli "id"
	var constraints = constraints;

	var validateResult = validate($(".validateFormAction"), constraints);
	// manage form errors
	return manageFormError(validateResult);
}

function manageFormError(validateResult) {
	var returnVar = true;
	// console.log("manageFormError function");
	// console.log(validateResult);
	if (validateResult && Object.keys(validateResult).length) {
		for (var property in validateResult) {
			if (validateResult.hasOwnProperty(property)) {
				// console.log("property: " + property);
				$("." + property + "Group").addClass("has-error");
				// TODO
				// eventualmente aggiungere il messaggio di errore in un blocco superiore

				// se presente anche un solo errore, blocco il submit del form
				returnVar = false;
			}
		}
	}

	return returnVar;
}

// TODO
function clearFormErrorClasses() {
	$(".formGroupAction").removeClass("has-error");

	return true;
}

/* Object to manage law cookie div */
// Creare's 'Implied Consent' EU Cookie Law Banner v:2.4
// Conceived by Robert Kent, James Bavington & Tom Foyster
var lawCookieCompliance = {
	dropCookie : true, // false disables the Cookie, allowing you to style the banner
	cookieDuration : 60, // Number of days before the cookie expires, and the banner reappears
	cookieName : 'complianceCookie', // Name of our cookie
	cookieValue : 'on', // Value of cookie

	createDiv : function() {
		var bodytag = document.getElementsByTagName('body')[0];
		var div = document.createElement('div');
		div.setAttribute('id', 'cookie-law');
		div.innerHTML = '<p>Su questo sito utilizziamo i cookie. Per saperne di più <a href="/cookie-policy" rel="nofollow" title="Cookies Policy">clicca qui</a>. Continuando la navigazione acconsenti al loro utilizzo.&nbsp;&nbsp;<a class="close-cookie-banner" href="javascript:void(0);" onclick="lawCookieCompliance.removeMe();"><span>X</span></a></p>';
		// bodytag.appendChild(div); // Adds the Cookie Law Banner just before the closing </body> tag
		// or
		bodytag.insertBefore(div, bodytag.firstChild); // Adds the Cookie Law Banner just after the opening <body> tag
		document.getElementsByTagName('body')[0].className += ' cookiebanner'; //Adds a class tothe <body> tag when the banner is visible
		this.createCookie(lawCookieCompliance.cookieName, lawCookieCompliance.cookieValue, lawCookieCompliance.cookieDuration); // Create the cookie
	},

	createCookie : function(name, value, days) {
		if (days) {
			var date = new Date();
			date.setTime(date.getTime()+(days*24*60*365*1000)); // 1 anno
			var expires = "; expires="+date.toGMTString(); 
		} else var expires = "";
		if(lawCookieCompliance.dropCookie) { 
			document.cookie = name+"="+value+expires+"; path=/"; 
		}
	},

	checkCookie : function(name) {
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++) {
			var c = ca[i];
			while (c.charAt(0)==' ') c = c.substring(1,c.length);
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
		}
		return null;
	},

	eraseCookie : function(name) {
		this.createCookie(name,"",-1);
	},

	removeMe : function() {
		var element = document.getElementById('cookie-law');
		if(element) element.parentNode.removeChild(element);
	},

	createDivOnLoad : function() {
		if(this.checkCookie(lawCookieCompliance.cookieName) != lawCookieCompliance.cookieValue){
			this.createDiv(); 
		}
	},
};
