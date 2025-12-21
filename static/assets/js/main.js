$(function () {

    ///نمایش زیر منو
    $(".showSubMenu").click(function () {
        $(this).nextAll("ul").toggleClass("show");
        $(this).toggleClass('open');
    })

    ///نمایش مگامنو آپدیدت جدید
    $(".main-menu-head").hover(function () {
        $(this).children().find(".main-menu-sub").first().addClass('main-menu-sub-active');
        $(this).children().addClass('active');
    })
    $(".main-menu-head").mouseleave(function () {
        $(this).children().find(".main-menu-sub").first().removeClass('main-menu-sub-active');
        $(this).children().removeClass('active');
    })
    $(".main-menu li").mouseover(function () {

        $(".main-menu li").removeClass("main-menu-sub-active-li");
        $(this).addClass("main-menu-sub-active-li");
        $(".main-menu-sub").removeClass('main-menu-sub-active');
        $(this).children('ul').removeClass('main-menu-sub-active');
        $(this).children('ul').addClass('main-menu-sub-active');
    });
    $(".main-menu-sub-active").mouseleave(function () {
        $(".main-menu-sub-active").removeClass("main-menu-sub-active");
    })

    ///شمارنده محصول برای اضافه کردن به سبد خرید
    $("input.counter").TouchSpin({
        min: 1,
        max: '1000000000000000',
        buttondown_class: "btn-counter waves-effect waves-light",
        buttonup_class: "btn-counter waves-effect waves-light"
    });

    ///انتخاب گر رنگ
    $(".category-sort .form-checks .form-check").click(function () {
        $(".category-sort .form-checks .form-check").removeClass("active");
        $(this).addClass('active');
        $(".category-sort .form-checks .form-check").children("input[type=radio]").attr('checked', false);
        $(this).children("input[type=radio]").attr('checked', true);
    })


    ///انتخاب زمان ارسال
    $(".send-item").click(function () {
        $(".send-item").removeClass("active");
        $(this).addClass('active');
    })

    ///انتخاب روش پستی
    $(".shipping-item").click(function () {
        $(".shipping-item").removeClass("active");
        $(this).addClass('active');
    })

    ///انتخاب روش پرداخت
    $(".bank-item").click(function () {
        $(".bank-item").removeClass("active");
        $(this).addClass('active');
    })


    jQuery('[data-bs-toggle="tooltip"]').tooltip();
    jQuery('[data-bs-toggle="modal"][title]').tooltip();

});

// function loginOtp() {
//     // var $link = $('#login_otp').find('a');
//     $("#id_mobile").addEventListener("input", function (event) {
//         let href = event.target.value
//         console.log(href)
//         $('#login_otp').attr('href', `/login/set_otp/${href}`);
//     })
// }

// function loginOtp() {
//     const phone = document.getElementById('id_mobile').value;
//     const link = document.getElementById('login_otp');
//     if (phone) {
//         link.href = `/login/set_otp/${phone}`;
//     } else {
//         link.href = '#';
//     }
// }

function goToOtp(next,event) {
    event.preventDefault();
    const phone = document.getElementById('id_mobile').value;
    if (!phone) {
        alert("لطفاً شماره موبایل را وارد کنید.");
    }
    fetch(`/api/authentication_module/set_otp/${phone}${next ? `?next=${next}` : ''}`, {
        method: 'GET',
    }).then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.url;
            } else if (data.status === 'mobile_not_valid') {
                Swal.fire({
                    title: 'خطا',
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "باشه",
                });
            } else if (data.status === 'user_not_found') {
                Swal.fire({
                    title: 'خطا',
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "باشه",
                });
            } else if (data.status === 'sms_send_failed') {
                Swal.fire({
                    title: 'خطا',
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "باشه",
                });
            }
        }).catch(error => console.log(error));
}

/**
 * open search form flaot
 */

$(document).ready(function () {

    /**
     * open
     */
    $(".header-search").click(function () {
        $(".search-float").toggleClass("open");
    });

    /**
     * close
     */

    $(".search-float-close").click(function () {
        $(".search-float").toggleClass("open");
    });


});

/**
 * open basket float with click
 */

$(document).ready(function () {

    /**
     * open
     */
    $(".header-cart-icon-toggle").click(function () {
        $(".min-cart").toggleClass("open");
    });

});


/**
 * config floating contact
 */
$('#btncollapzion').Collapzion({
    _child_attribute: [{
        'label': 'پشتیبانی تلفنی',
        'url': 'tel:0930555555555',
        'icon': 'bi bi-telephone'
    },
        {
            'label': 'پشتیبانی تلگرام',
            'url': 'https://tlgrm.me',
            'icon': 'bi bi-telegram'
        },
        {
            'label': 'پشتیبانی واتس آپ',
            'url': 'https://wa.me/444444444',
            'icon': 'bi-whatsapp'
        },

    ],
});


// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

/*
*
* mega menu floating
*
* */
$(function () {
    var lastScrollTop = 0, delta = 50;
    $(window).scroll(function () {
        var nowScrollTop = $(this).scrollTop();
        if (Math.abs(lastScrollTop - nowScrollTop) >= delta) {
            if (nowScrollTop > lastScrollTop) {
                // ACTION ON
                // SCROLLING DOWN
                $(".mega-menu").removeClass("mega-menu-top");
                //$(".header").addClass("shadow-md pb-3");
            } else {
                // ACTION ON
                // SCROLLING UP
                $(".mega-menu").addClass("mega-menu-top");
                //$(".header").removeClass("shadow-md pb-3");
            }
            lastScrollTop = nowScrollTop;
        }
    });
});


/**
 * delivery item form check
 */

$(document).ready(function () {

    $(".delivery-item").click(function () {
        $(this).find('input').prop("checked", true);
    });

    $(".delivary-payment-bank-item").click(function () {
        $(".delivary-payment-bank-item").removeClass("active");
        $(this).addClass("active");
    });
});


$(document).ready(function () {
    $(".step-passwd").hide();
    $(".step-two").hide();

    $(".step-one").click(function () {
        $(this).hide();
        $(".step-passwd").show();
        $(".step-two").show();
    })
})
