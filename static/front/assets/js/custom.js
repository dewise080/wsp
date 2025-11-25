(function($) {
    "use strict";
    var cursor = document.querySelector('.cursor');
    var cursorinner = document.querySelector('.cursor2');
    var a = document.querySelectorAll('a');
    document.addEventListener('mousemove', function(e) {
        var x = e.clientX;
        var y = e.clientY;
        cursor.style.transform = `translate3d(calc(${e.clientX}px - 50%), calc(${e.clientY}px - 50%), 0)`
    });
    $('a').hover(function() {
        $('.cursor').css({});
    }, function() {
        $('.cursor2').css({
            "background-color": "#fff"
        });
    });
    jQuery(window).on('load', function() {
        $(".preloader").delay(1600).fadeOut("slow");
    });
    const currentLocation = location.href;
    const menuItem = document.querySelectorAll('ul li a');
    const menuLength = menuItem.length;
    for (let i = 0; i < menuLength; i++) {
        if (menuItem[i].href === currentLocation) {
            menuItem[i].className = "active";
        }
    }
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 200) {
            $('.position_top').addClass('sticky');
        } else {
            $('.position_top').removeClass('sticky');
        }
    });
    $('.cross-btn').on('click', function(event) {
        $('.main-nav').toggleClass('slidenav');
    });
    $('.remove').on('click', function(event) {
        $('.main-nav').removeClass('slidenav');
    });
    $(".main-nav .bi").on('click', function(event) {
        var $fl = $(this);
        $(this).parent().siblings().find('.sub-menu').slideUp();
        $(this).parent().siblings().find('.bi').addClass('bi-chevron-down');
        if ($fl.hasClass('bi-chevron-down')) {
            $fl.removeClass('bi-chevron-down').addClass('bi-chevron-up');
        } else {
            $fl.removeClass('bi-chevron-up').addClass('bi-chevron-down');
        }
        $fl.next(".sub-menu").slideToggle();
    });
    $('.tab-link').on('click', function(event) {
        $('.tab-link').removeClass('active');
        $(this).addClass('active');
    });

    $('ul.isotope-menu li').on('click', function() {
        $("ul.isotope-menu li").removeClass("active");
        $(this).addClass("active");
        var selector = $(this).attr('data-filter');
        $(".project-items").isotope({
            filter: selector,
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false,
            }
        });
        return false;
    });
    $('.video-popup').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });
    var swiper = new Swiper(".team-slider", {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 30,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            }
        }
    });
    var swiper = new Swiper(".project-slide", {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 30,
        navigation: {
            nextEl: ".swiper-button-next-c",
            prevEl: ".swiper-button-prev-c",
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 0,
            },
            576: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            }
        }
    });
    var swiper = new Swiper(".work-process-slide", {
        loop: true,
        slidesPerView: 1,
        navigation: {
            nextEl: ".swiper-button-next-c",
            prevEl: ".swiper-button-prev-c",
        }
    });
    var swiper = new Swiper(".testimonial-slider", {
        loop: true,
        slidesPerView: 2,
        centeredSlides: true,
        speed: 1000,
        spaceBetween: 30,
        slideToClickedSlide: true,
        autoplay: {
            delay: 5000
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 2,
            },
            1400: {
                slidesPerView: 2,
            },
            1800: {
                slidesPerView: 2,
            }
        }
    });
    var swiper = new Swiper(".partner-slider", {
        loop: true,
        slidesPerView: 5,
        spaceBetween: 20,
        navigation: {
            nextEl: '.swiper-button-next-c',
            prevEl: '.swiper-button-prev-c',
        },
        breakpoints: {
            320: {
                slidesPerView: 2,
            },
            576: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 4,
            },
            1200: {
                slidesPerView: 5,
            }
        }
    });
    var swiper = new Swiper(".services-slider", {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 30,
        speed: 1000,
        autoplay: {
            delay: 5000
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            }
        }
    });
    var swiper = new Swiper(".hero-slide", {
        loop: false,
        slidesPerView: 1,
        spaceBetween: 30,
        speed: 1000,
        autoplay: {
            delay: 5000
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 1,
            },
            992: {
                slidesPerView: 1,
            }
        }
    });
    jQuery(window).on('load', function() {
        new WOW().init();
        window.wow = new WOW({
            boxClass: 'wow',
            animateClass: 'animated',
            offset: 0,
            mobile: true,
            live: true,
            offset: 100
        })
        window.wow.init();
    });
}(jQuery));

/* Back to top */
let calcScrollValue = () => {
    let scrollProgress = document.getElementById("progress");
    let progressValue = document.getElementById("progress-value");
    let pos = document.documentElement.scrollTop;
    let calcHeight =
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight;
    let scrollValue = Math.round((pos * 100) / calcHeight);
    if (pos > 100) {
      scrollProgress.style.display = "grid";
    } else {
      scrollProgress.style.display = "none";
    }
    scrollProgress.addEventListener("click", () => {
      document.documentElement.scrollTop = 0;
    });
    scrollProgress.style.background = `conic-gradient(#75dab4 ${scrollValue}%, #d7d7d7 ${scrollValue}%)`;
  };
  
  window.onscroll = calcScrollValue;
  window.onload = calcScrollValue;

const counters = document.querySelectorAll('.counter');
const speed = 200; // The lower the slower

counters.forEach(counter => {
    const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        let count = +counter.innerText;

        // Calculate the increment based on the difference between target and current count
        const diff = target - count;
        const increment = diff > 0 ? Math.ceil(diff / (speed / 10)) : -Math.ceil(-diff / (speed / 10));

        // Calculate the timeout based on the increment and target value
        const timeout = Math.abs(diff) > 100 ? 10 : 100;

        // Check if target is reached
        if (count !== target) {
            // Add increment to count and output in counter
            count += increment;
            counter.innerText = count;
            // Call function with adjusted timeout
            setTimeout(updateCount, timeout);
        }
    };

    // Initialize count to 0
    counter.innerText = '0';
    
    // Start the updateCount function
    updateCount();
});






