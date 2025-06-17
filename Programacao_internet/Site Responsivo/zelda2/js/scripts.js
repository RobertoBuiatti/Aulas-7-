window.addEventListener('scroll', function() {
	var wScroll = window.pageYOffset || document.documentElement.scrollTop;
	
	document.querySelector('.movimento-poster').style.backgroundPosition = 'right ' + (wScroll * 0.75) + 'px';
	
	document.querySelector('.movimento-textbox').style.top = (-8 + (wScroll * 0.005)) + 'em';
});