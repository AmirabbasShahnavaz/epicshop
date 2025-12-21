$(function () {
    const $input = $("#search_input");
    $input.autocomplete({
        source: function (request, response) {
            if (request.term.length < 2) {
                return response([]);
            }

            $.ajax({
                url: "/products/search",
                data: {q: request.term},
                success: function (data) {
                    if (!data.length) {
                        response([{label: "محصولی یافت نشد", value: ""}]);
                        return;
                    }

                    const term = request.term.toLowerCase();

                    const results = data.map(item => {
                        const title = item.title;
                        const regex = new RegExp("(" + term + ")", "gi");
                        const highlighted = title.replace(regex, '<strong>$1</strong>');

                        return {
                            label: highlighted,  // این HTMLی میشه
                            value: title,
                            category: "سلام من دسته بندی هستم",
                        };
                    });

                    response(results);
                }
            });
        },
        minLength: 2,
        select: function (event, item) {
            $("#search_input").val(item.item.value);
            $("#form_search").submit();
        },
        focus: function (event, ui) {
            if (!ui.item.value) {
                event.preventDefault();
            }
        }
    }).data("ui-autocomplete")._renderItem = function (ul, item) {
        return $("<li>")
            .append(`<div>${item.label}</div>`)
            .appendTo(ul);
    };

    const $input_mobile = $("#search_input_mobile");
    $input_mobile.autocomplete({
        source: function (request, response) {
            if (request.term.length < 2) {
                return response([]);
            }

            $.ajax({
                url: "/products/search",
                data: {q: request.term},
                success: function (data) {
                    if (!data.length) {
                        response([{label: "محصولی یافت نشد", value: ""}]);
                        return;
                    }
                    let results = data.map(item => ({
                        label: item.title,
                        value: item.title,
                        category: item.category,
                    }));
                    response(results);
                }
            });
        },
        minLength: 2,
        select: function (event, item) {
            $("#search_input_mobile").val(item.item.value);
            $("#form_search_mobile").submit();
        },
        focus: function (event, ui) {
            if (!ui.item.value) {
                event.preventDefault();
            }
        }
    });
});


// function initPriceSlider(min, max, startMin, startMax) {
//     const allSliders = document.querySelectorAll('.price-slider');
//
//     allSliders.forEach(slider => {
//         if (slider.classList.contains('initialized')) return;
//
//         const wrapper = slider.closest('.filter-box');
//         const minText = wrapper.querySelector('.min-price');
//         const maxText = wrapper.querySelector('.max-price');
//         const minInput = wrapper.querySelector('.price-min');
//         const maxInput = wrapper.querySelector('.price-max');
//
//         noUiSlider.create(slider, {
//             start: [startMin, startMax],
//             connect: true,
//             direction: 'rtl',
//             step: 10000,
//             range: {
//                 'min': min,
//                 'max': max
//             },
//             format: {
//                 to: value => Math.round(value),
//                 from: value => Number(value)
//             }
//         });
//
//         slider.noUiSlider.on('update', function (values) {
//             minText.textContent = Number(values[0]).toLocaleString('fa-IR');
//             maxText.textContent = Number(values[1]).toLocaleString('fa-IR');
//             minInput.value = values[0];
//             maxInput.value = values[1];
//         });
//
//         slider.noUiSlider.on('change', function () {
//             range_filter();
//         });
//
//         slider.classList.add('initialized');
//     });
// }

function initPriceSlider(min, max, startMin, startMax) {
    const allSliders = document.querySelectorAll('.price-slider');
    const sliders = [];

    allSliders.forEach(slider => {
        if (slider.classList.contains('initialized')) return;

        const wrapper = slider.closest('.filter-box');
        const minText = wrapper.querySelector('.min-price');
        const maxText = wrapper.querySelector('.max-price');
        const minInput = wrapper.querySelector('.price-min');
        const maxInput = wrapper.querySelector('.price-max');

        noUiSlider.create(slider, {
            start: [startMin, startMax],
            connect: true,
            direction: 'rtl',
            step: 10000,
            range: {
                'min': min,
                'max': max
            },
            format: {
                to: value => Math.round(value),
                from: value => Number(value)
            }
        });

        // ذخیره برای همگام‌سازی
        sliders.push(slider.noUiSlider);

        slider.noUiSlider.on('update', function (values) {
            minText.textContent = Number(values[0]).toLocaleString('fa-IR');
            maxText.textContent = Number(values[1]).toLocaleString('fa-IR');
            minInput.value = values[0];
            maxInput.value = values[1];
        });

        slider.noUiSlider.on('change', function (values) {
            // همگام‌سازی با بقیه اسلایدرها
            sliders.forEach(otherSlider => {
                if (otherSlider !== slider.noUiSlider) {
                    otherSlider.set(values);
                }
            });

            // اجرای تابع فیلتر (اختیاری)
            range_filter();
        });

        slider.classList.add('initialized');
    });
}


function separate(Number) {
    Number += '';
    Number = Number.replace(',', '');
    x = Number.split('.');
    y = x[0];
    z = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(y))
        y = y.replace(rgx, '$1' + ',' + '$2');
    return y + z;
}

function range_filter() {
    setTimeout(priceRange, 700);

    function priceRange() {
        submit_form()
    }
}

function submit_form(selector = 'list_form') {
    $(`#${selector}`).submit();
}

function submit_form_value(ipt_selector, selector_value, selector = 'list_form') {
    $(`#${ipt_selector}`).val(selector_value);
    $(`#${selector}`).submit();
}

function submit_form_question(selector = 'basket_form', is_cancel = false) {
    if (is_cancel) {
        Swal.fire({
            title: 'انصراف از سفارش',
            text: 'آیا از انصراف سفارش اطمینان دارید؟.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'بله، انصراف میدم',
            cancelButtonText: 'خیر، منصرف شدم',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                $(`#${selector}`).submit();
            }
        })
    } else {
        Swal.fire({
            title: 'حذف آیتم',
            text: 'آیا از حذف این آیتم اطمینان دارید؟.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'بله، حذف شود',
            cancelButtonText: 'خیر، منصرف شدم',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                $(`#${selector}`).submit();
            }
        })
    }
}


function submit_form_3(p_id, c_id) {
    $('#c_id').val(c_id);
    $('#p_id').val(p_id);
    $('#basket_add_form').submit();
}

function sort_by_filter(sortBy) {
    $('#id_sort_by').val(sortBy);
    submit_form()
}

function sortInputTargets() {
    const isMobile = window.innerWidth <= 991;
    const select = document.getElementById('sort-select-mobile');
    const hiddenInput = document.getElementById('id_sort_by');

    if (isMobile) {
        hiddenInput.removeAttribute('name');
        select.setAttribute('name', 'sort_by');
    } else {
        select.removeAttribute('name');
        hiddenInput.setAttribute('name', 'sort_by');
    }
}

let previouslyDisabledInput = null;

function change_color(p_id, color_id, counter) {
    if (previouslyDisabledInput) {
        previouslyDisabledInput.disabled = false;
    }

    const selectedInput = document.getElementById(`color_${counter}`);
    selectedInput.disabled = true;
    previouslyDisabledInput = selectedInput;

    fetch(`/products/d/change_color/${color_id}/${p_id}`).then(r => r.json())
        .then(data => {
            if (data.status !== 'failed') {
                document.getElementById('ppo').innerText = separate(data.price) + " تومان";
                document.getElementById('ppt').innerText = separate(data.price) + " تومان";
                document.getElementById('c_id').value = color_id;
            }

        }).catch(err => console.log(err));
}

function increase_basket_quantity(product_id, color_id) {
    fetch(`/api/order_module/basket/increase-quantity/${product_id}/${color_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById('csrf_token').value
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('درخواست شما با شکست مواجه شد لطفا دوباره تلاش کنید');
            }
            return response.json();
        }).then(data => {
        if (data.status === 'success') {
            $(".box1").load(location.href + " .box2");
        } else if (data.status === 'quantity_limited') {
            Swal.fire({
                title: 'خطا',
                text: data.message,
                icon: "error",
                confirmButtonText: "باشه",
            });
        } else if (data.status === 'basket_not_found') {
            Swal.fire({
                title: 'خطا',
                text: data.message,
                icon: "error",
                confirmButtonText: "باشه",
            });
        }
    })
}

function decrease_basket_quantity(product_id, color_id, is_final = false) {
    if (is_final) {
        Swal.fire({
            title: 'حذف آیتم',
            text: 'آیا از حذف این آیتم اطمینان دارید؟.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'بله، حذف شود',
            cancelButtonText: 'خیر، منصرف شدم',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/api/order_module/basket/decrease-quantity/${product_id}/${color_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.getElementById('csrf_token').value
                    }
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('درخواست شما با شکست مواجه شد لطفا دوباره تلاش کنید');
                        }
                        return response.json();
                    }).then(data => {
                    if (data.status === 'success') {
                        $(".box1").load(location.href + " .box2");
                    } else if (data.status === 'basket_removed') {
                        location.reload();
                    } else if (data.status === 'basket_not_found') {
                        Swal.fire({
                            title: 'خطا',
                            text: data.message,
                            icon: "error",
                            confirmButtonText: "باشه",
                        });
                    }
                })
            }
        });
    } else {
        fetch(`/api/order_module/basket/decrease-quantity/${product_id}/${color_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf_token').value
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('درخواست شما با شکست مواجه شد لطفا دوباره تلاش کنید');
                }
                return response.json();
            }).then(data => {
            if (data.status === 'success') {
                $(".box1").load(location.href + " .box2");
            } else if (data.status === 'basket_removed') {
                location.reload();
            } else if (data.status === 'basket_not_found') {
                Swal.fire({
                    title: 'خطا',
                    text: data.message,
                    icon: "error",
                    confirmButtonText: "باشه",
                });
            }
        })
    }
}

function delete_basket_product(product_id, color_id) {
    Swal.fire({
        title: 'حذف آیتم',
        text: 'آیا از حذف این آیتم اطمینان دارید؟.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله، حذف شود',
        cancelButtonText: 'خیر، منصرف شدم',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/api/order_module/basket/destroy/${product_id}/${color_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.getElementById('csrf_token').value
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('درخواست شما با شکست مواجه شد لطفا دوباره تلاش کنید');
                    }
                    return response.json();
                }).then(data => {
                if (data.status === 'success') {
                    location.reload();
                } else if (data.status === 'basket_not_found') {
                    Swal.fire({
                        title: 'خطا',
                        text: data.message,
                        icon: "error",
                        confirmButtonText: "باشه",
                    });
                }
            })
        }
    });
}

function handle_payment() {
    const walletInput = document.getElementById("wallet");
    const walletBox = document.getElementById("wallet-balance-box");

    if (walletInput.checked) {
        walletBox.style.display = "block";
    } else {
        walletBox.style.display = "none";
    }
}

function pay_submit(wallet_amount, pay_amount) {
    const walletSelected = document.getElementById("wallet").checked;
    $("#first_name_ipt").val($("#id_first_name").val());
    $("#last_name_ipt").val($("#id_last_name").val());
    if (walletSelected) {
        if (wallet_amount < pay_amount) {
            Swal.fire({
                icon: 'error',
                title: 'موجودی کافی نیست',
                text: 'موجودی کیف پول شما کمتر از مبلغ پرداخت است.',
                confirmButtonText: 'باشه',
            });
            return;
        }

        Swal.fire({
            title: 'پرداخت با کیف پول',
            html: `مبلغ <strong>${pay_amount}</strong> تومان از موجودی <strong>${wallet_amount}</strong> کیف پول شما کسر خواهد شد.<br>آیا تأیید می‌کنید؟`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'بله، پرداخت کن',
            cancelButtonText: 'لغو',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById("pay_order_form").submit();
            }
        });
    } else {
        document.getElementById("pay_order_form").submit();
    }
}

function showPersianPricePreview(inputId, previewId, max = 100_000_000) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    const container = preview?.closest('.form-text');
    if (!input || !preview || !container) return;

    const format = new Intl.NumberFormat('fa-IR');
    let lastValue = null;

    function toReadablePersianAmount(num) {
        if (num > max) return 'بیشتر از حد داری میزنی!';

        const parts = [];
        const million = Math.floor(num / 1_000_000);
        const thousand = Math.floor((num % 1_000_000) / 1_000);
        const rial = num % 1_000;

        if (million) parts.push(`${format.format(million)} میلیون`);
        if (thousand) parts.push(`${format.format(thousand)} هزار`);
        if (rial) parts.push(`${format.format(rial)}`);

        return parts.length ? parts.join(' و ') + ' تومان' : '';
    }

    function update() {
        const raw = input.value.trim().replaceAll(',', '');
        const num = parseInt(raw);

        if (raw === lastValue) return; // فقط اگه مقدار جدید شد، آپدیت کن
        lastValue = raw;

        if (!isNaN(num)) {
            const result = toReadablePersianAmount(num);
            preview.textContent = result;
            container.classList.remove('d-none');
            container.classList.toggle('text-danger', num > max);
            container.classList.toggle('text-secondary', num <= max);
        } else {
            preview.textContent = '';
            container.classList.add('d-none');
        }
    }

    input.addEventListener('input', update);
    update();
}


function add_to_favorite(product_id) {
    fetch(`/products/add_to_favorite/${product_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementById('csrf_token').value
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('درخواست شما با شکست مواجه شد لطفا دوباره تلاش کنید');
            }
            return response.json();
        }).then(data => {
        if (data.status === 'success') {
            $(`.box1`).load(location.href + ` .box2`, function () {
                $(".boxa").load(location.href + " .boxb");
            });
            Swal.fire({
                title: 'موفقیت',
                text: data.message,
                icon: "success",
                confirmButtonText: "باشه",
            });
        } else if (data.status === 'is_not_authenticated') {
            Swal.fire({
                title: 'خطا',
                text: data.message,
                icon: "error",
                confirmButtonText: "باشه",
            });
        } else if (data.status === 'product_not_found') {
            Swal.fire({
                title: 'خطا',
                text: data.message,
                icon: "error",
                confirmButtonText: "باشه",
            });
        }
    })
}

function fill_page(paging_id) {
    $('#paging_ipt').val(paging_id);
    submit_form()
}

function load_ticket_modal() {
    $.ajax({
        url: `/user_panel/tickets/create`,
        type: "get",
        success: function (response) {
            if (response.status === "no_complete")
                window.location.href = response.url;

            $('#modal-body').html(response);
            $('#user-modal-title').text('ثبت تیکت جدید');
            $('#user-modal').modal('show');
        }
    });
}

function on_create_ticket(response) {
    if (response.status === "is_not_valid")
        return $('#modal-body').html(response.html);

    $('#user-modal').modal('hide');
    if (response.status === "success") {
        Swal.fire({
            title: 'موفقیت',
            text: response.message,
            icon: "success",
            confirmButtonText: "باشه",
        }).then(result => {
            location.reload();
        })
    } else if (response.status === "error") {
        Swal.fire({
            title: 'خطا',
            text: response.message,
            icon: "error",
            confirmButtonText: "باشه",
        }).then(result => {
            location.reload();
        })
    }
}

function submit_ticket_form() {
    $('#id_search').val($('#search_ipt').val());
    submit_form()
}

function submit_ticket_create() {
    const frm = document.getElementById('ticket-form')
    if (frm.checkValidity()) {
        $('#create_btn').remove()
        frm.dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
    } else {
        frm.reportValidity();
    }
}