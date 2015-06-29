jQuery(document).ready(function($) {
    //*** Detect Device ***//
    (function(document) {

        // for touch devices: add class cs-hover to the figures when touching the items
        if (Modernizr.touch) {

            // classie.js https://github.com/desandro/classie/blob/master/classie.js
            // class helper functions from bonzo https://github.com/ded/bonzo

            function classReg(className) {
                return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
            }

            // classList support for class management
            // altho to be fair, the api sucks because it won't accept multiple classes at once
            var hasClass, addClass, removeClass;

            if ('classList' in document.documentElement) {
                hasClass = function(elem, c) {
                    return elem.classList.contains(c);
                };
                addClass = function(elem, c) {
                    elem.classList.add(c);
                };
                removeClass = function(elem, c) {
                    elem.classList.remove(c);
                };
            } else {
                hasClass = function(elem, c) {
                    return classReg(c).test(elem.className);
                };
                addClass = function(elem, c) {
                    if (!hasClass(elem, c)) {
                        elem.className = elem.className + ' ' + c;
                    }
                };
                removeClass = function(elem, c) {
                    elem.className = elem.className.replace(classReg(c), ' ');
                };
            }

            function toggleClass(elem, c) {
                var fn = hasClass(elem, c) ? removeClass : addClass;
                fn(elem, c);
            }

            var classie = {
                // full names
                hasClass: hasClass,
                addClass: addClass,
                removeClass: removeClass,
                toggleClass: toggleClass,
                // short names
                has: hasClass,
                add: addClass,
                remove: removeClass,
                toggle: toggleClass
            };

            // transport
            if (typeof define === 'function' && define.amd) {
                // AMD
                define(classie);
            } else {
                // browser global
                window.classie = classie;
            }

            [].slice.call(document.querySelectorAll('#pf-wrapper2 > .item > figure, .block-grid li > .caption-style2 > figure, .block-grid-nomargin > .caption-style2 > figure')).forEach(function(el, i) {
                el.querySelector('figcaption > a').addEventListener('touchstart', function(e) {
                    e.stopPropagation();
                }, false);
                el.addEventListener('touchstart', function(e) {
                    classie.toggle(this, 'cs-hover');
                }, false);
            });

        }

    })(document);

    //*** Greyscale img ***//
    $(window).load(function() {
        $('.client-box img, #client-carousel img').each(function() {
            $(this).wrap('<div style="display:inline-block;width:' + this.width + 'px;height:' + this.height + 'px;">').clone().addClass('gotcolors').css({
                'position': 'absolute',
                'opacity': 0
            }).insertBefore(this);
            this.src = grayscale(this.src);
        }).animate({
            opacity: 1
        }, 500);
    });

    $(document).ready(function() {
        $(".client-box a, #client-carousel a").hover(
            function() {
                $(this).find('.gotcolors').stop().animate({
                    opacity: 1
                }, 200);
            },
            function() {
                $(this).find('.gotcolors').stop().animate({
                    opacity: 0
                }, 500);
            }
        );
    });

    function grayscale(src) {
        var supportsCanvas = !!document.createElement('canvas').getContext;
        if (supportsCanvas) {
            var canvas = document.createElement('canvas'),
                context = canvas.getContext('2d'),
                imageData, px, length, i = 0,
                gray,
                img = new Image();

            img.src = src;
            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0);

            imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            px = imageData.data;
            length = px.length;

            for (; i < length; i += 4) {
                gray = px[i] * .3 + px[i + 1] * .59 + px[i + 2] * .11;
                px[i] = px[i + 1] = px[i + 2] = gray;
            }

            context.putImageData(imageData, 0, 0);
            return canvas.toDataURL();
        } else {
            return src;
        }
    }

    //*** Mainmenu ***//
    $("ul#menu").superfish();

    //*** Newsticker ***//
    $("ul#newsticker").liScroll();

    //*** Countent Carousel ***//
    $('#client-carousel').carouFredSel({
        auto: false,
        responsive: true,
        width: '100%',
        prev: '#prev-carousel',
        next: '#next-carousel',
        scroll: 1,
        items: {
            width: 160,
            //	height: '30%',	//	optionally resize item-height
            visible: {
                min: 5,
                max: 5
            }
        }
    });

    $('#testi-carousel').carouFredSel({
        responsive: true,
        width: '100%',
        pagination: "#pager-carousel",
        scroll: {
            items: 1,
            timeoutDuration: 6000,
            pauseOnHover: false
        }

    });


    //*** Tabs on Top Jquery ***//
    $(".tab_content").hide();
    $("ul.tabs li:first").addClass("active").show();
    $(".tab_content:first").show();
    $("ul.tabs li").click(function() {
        $("ul.tabs li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).fadeIn();
        return false
    });


    //*** Tabs on Bottom Jquery ***//
    $(".tab_content-bottom").hide();
    $("ul.tabs-bottom li:first").addClass("active").show();
    $(".tab_content-bottom:first").show();
    $("ul.tabs-bottom li").click(function() {
        $("ul.tabs-bottom li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content-bottom").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).fadeIn();
        return false
    });


    //*** Tabs on Left Jquery ***//
    $(".tab_content-left").hide();
    $("ul.tabs-left li:first").addClass("active").show();
    $(".tab_content-left:first").show();
    $("ul.tabs-left li").click(function() {
        $("ul.tabs-left li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content-left").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).fadeIn();
        return false
    });


    //*** Tabs on Right Jquery ***//
    $(".tab_content-right").hide();
    $("ul.tabs-right li:first").addClass("active").show();
    $(".tab_content-right:first").show();
    $("ul.tabs-right li").click(function() {
        $("ul.tabs-right li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content-right").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).fadeIn();
        return false
    });

    //*** Tabs round Jquery ***//
    $(".tab_content-round").hide();
    $("ul.tabs-round li:first").addClass("active").show();
    $(".tab_content-round:first").show();
    $("ul.tabs-round li").click(function() {
        $("ul.tabs-round li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content-round").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).fadeIn();
        return false
    });


    //*** Fancybox Jquery ***//
    $(".fancybox").fancybox({
        padding: 0,
        openEffect: 'elastic',
        openSpeed: 250,
        closeEffect: 'elastic',
        closeSpeed: 250,
        closeClick: false,
        helpers: {
            title: {
                type: 'outside'
            },
            overlay: {
                css: {
                    'background': 'rgba(0,0,0,0.85)'
                }
            },
            media: {}
        }
    });


    //*** TinyNav Jquery ***//
    (function(a, i, g) {
        a.fn.tinyNav = function(j) {
            var b = a.extend({
                active: "selected",
                header: "",
                label: ""
            }, j);
            return this.each(function() {
                g++;
                var h = a(this),
                    d = "tinynav" + g,
                    f = ".l_" + d,
                    e = a("<select/>").attr("id", d).addClass("tinynav " + d);
                if (h.is("ul,ol")) {
                    "" !== b.header && e.append(a("<option/>").text(b.header));
                    var c = "";
                    h.addClass("l_" + d).find("a").each(function() {
                        c += '<option value="' + a(this).attr("href") + '">';
                        var b;
                        for (b = 0; b < a(this).parents("ul, ol").length - 1; b++) c += "- ";
                        c += a(this).text() + "</option>"
                    });
                    e.append(c);
                    b.header || e.find(":eq(" + a(f + " li").index(a(f + " li." + b.active)) + ")").attr("selected", !0);
                    e.change(function() {
                        i.location.href = a(this).val()
                    });
                    a(f).after(e);
                    b.label && e.before(a("<label/>").attr("for", d).addClass("tinynav_label " + d + "_label").append(b.label))
                }
            })
        }
    })(jQuery, this, 0);
    $('#menu').tinyNav({
        active: 'selected',
        header: 'Navigation'
    });


    //*** Search Panel ***//
    $(".trigger").click(function() {
        $(".search-panel").toggle("fast");
        $(this).toggleClass("active");
        return false
    });


    //*** Tooltip Jquery ***//
    var targets = $('[class=tooltip]'),
        target = false,
        tooltip = false,
        title = false;
    targets.bind('mouseenter', function() {
        target = $(this);
        tip = target.attr('title');
        tooltip = $('<div id="tooltip"></div>');
        if (!tip || tip == '') return false;
        target.removeAttr('title');
        tooltip.css('opacity', 0).html(tip).appendTo('body');
        var init_tooltip = function() {
            if ($(window).width() < tooltip.outerWidth() * 1.5) tooltip.css('max-width', $(window).width() / 2);
            else tooltip.css('max-width', 340);
            var pos_left = target.offset().left + (target.outerWidth() / 2) - (tooltip.outerWidth() / 2),
                pos_top = target.offset().top - tooltip.outerHeight() - 20;
            if (pos_left < 0) {
                pos_left = target.offset().left + target.outerWidth() / 2 - 20;
                tooltip.addClass('left')
            } else tooltip.removeClass('left');
            if (pos_left + tooltip.outerWidth() > $(window).width()) {
                pos_left = target.offset().left - tooltip.outerWidth() + target.outerWidth() / 2 + 20;
                tooltip.addClass('right')
            } else tooltip.removeClass('right');
            if (pos_top < 0) {
                var pos_top = target.offset().top + target.outerHeight();
                tooltip.addClass('top')
            } else tooltip.removeClass('top');
            tooltip.css({
                left: pos_left,
                top: pos_top
            }).animate({
                top: '+=10',
                opacity: 1
            }, 50)
        };
        init_tooltip();
        $(window).resize(init_tooltip);
        var remove_tooltip = function() {
            tooltip.animate({
                top: '-=10',
                opacity: 0
            }, 50, function() {
                $(this).remove()
            });
            target.attr('title', tip)
        };
        target.bind('mouseleave', remove_tooltip);
        tooltip.bind('click', remove_tooltip);
    });


    //*** To top Jquery ***//
    (function($) {
        $.fn.UItoTop = function(options) {
            var defaults = {
                    text: '<i class="icon-chevron-up"></i>',
                    min: 200,
                    inDelay: 600,
                    outDelay: 400,
                    containerID: 'toTop',
                    containerHoverID: 'toTopHover',
                    scrollSpeed: 1200,
                    easingType: 'linear'
                },
                settings = $.extend(defaults, options),
                containerIDhash = '#' + settings.containerID,
                containerHoverIDHash = '#' + settings.containerHoverID;
            $('body').append('<a href="#" id="' + settings.containerID + '">' + settings.text + '</a>');
            $(containerIDhash).hide().on('click.UItoTop', function() {
                $('html, body').animate({
                    scrollTop: 0
                }, settings.scrollSpeed, settings.easingType);
                $('#' + settings.containerHoverID, this).stop().animate({
                    'opacity': 0
                }, settings.inDelay, settings.easingType);
                return false;
            }).prepend('<span id="' + settings.containerHoverID + '"></span>').hover(function() {
                $(containerHoverIDHash, this).stop().animate({
                    'opacity': 1
                }, 600, 'linear');
            }, function() {
                $(containerHoverIDHash, this).stop().animate({
                    'opacity': 0
                }, 700, 'linear');
            });
            $(window).scroll(function() {
                var sd = $(window).scrollTop();
                if (typeof document.body.style.maxHeight === "undefined") {
                    $(containerIDhash).css({
                        'position': 'absolute',
                        'top': sd + $(window).height() - 50
                    });
                }
                if (sd > settings.min)
                    $(containerIDhash).fadeIn(settings.inDelay);
                else
                    $(containerIDhash).fadeOut(settings.Outdelay);
            });
        };
    })(jQuery);
    $().UItoTop({
        easingType: 'easeOutQuart'
    });


    //*** Progress Bar Jquery ***//
    function progress(percent, element) {
        var progressBarWidth = percent * element.width() / 100;
        element.find('div').animate({
            width: progressBarWidth
        }, 2000).html("<div class='progress-meter'>" + percent + "%&nbsp;</div>");
    }

    $(document).ready(function() {
        $('.progress-bar').each(function() {
            var bar = $(this);
            var percentage = $(this).attr('data-percent');

            progress(percentage, bar);
        });
    });

    //*** Weather ***//
    $(document).ready(function() {
        $.simpleWeather({
            zipcode: '',
            woeid: '26812346',
            location: '',
            unit: 'c',
            success: function(weather) {
                html = '<img style="float:left;" width="100px" src="' + weather.image + '">';
                html += '<h3>' + weather.city + ', ' + weather.region + '</h3>';
                html += '<p>' + weather.temp + '&deg; ' + weather.units.temp + ' &nbsp; ' + weather.currently + '</p>';

                $("#weather").html(html);
            },
            error: function(error) {
                $("#weather").html('<p>' + error + '</p>');
            }
        });
    });

    //*** Media element Player Jquery ***//
    $('audio,video').mediaelementplayer();

        //Slideshow
    $('.banner-blog').revolution({
        delay:9000,
        onHoverStop:"off",// Stop Banner Timet at Hover on Slide on/off
        thumbWidth:100,// Thumb With and Height and Amount (only if navigation Tyope set to thumb !)
        thumbHeight:50,
        thumbAmount:3,
        hideThumbs:0,
        navigationType:"bullet",// bullet, thumb, none
        navigationArrows:"none",// nexttobullets, solo (old name verticalcentered), none
        navigationStyle:"round-old",// round,square,navbar,round-old,square-old,navbar-old, or any from the list in the docu (choose between 50+ different item), custom
        navigationHAlign:"right",// Vertical Align top,center,bottom
        navigationVAlign:"top",// Horizontal Align left,center,right
        navigationHOffset:40,
        navigationVOffset:28,
        touchenabled:"on",// Enable Swipe Function : on/off
        stopAtSlide:-1,// Stop Timer if Slide "x" has been Reached. If stopAfterLoops set to 0, then it stops already in the first Loop at slide X which defined. -1 means do not stop at any slide. stopAfterLoops has no sinn in this case.
        stopAfterLoops:-1,// Stop Timer if All slides has been played "x" times. IT will stop at THe slide which is defined via stopAtSlide:x, if set to -1 slide never stop automatic
        hideCaptionAtLimit:0,// It Defines if a caption should be shown under a Screen Resolution ( Basod on The Width of Browser)
        hideAllCaptionAtLilmit:0,// Hide all The Captions if Width of Browser is less then this value
        hideSliderAtLimit:0,// Hide the whole slider, and stop also functions if Width of Browser is less than this value
        fullWidth:"0ff",
        shadow:0//0 = no Shadow, 1,2,3 = 3 Different Art of Shadows -  (No Shadow in Fullwidth Version !)
    })

});