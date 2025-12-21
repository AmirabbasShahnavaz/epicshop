$('#province_id').on("change", function () {
    var provinceId = $('#province_id').val();
    if (provinceId !== '0') {
        $.ajax({
            url: `/user_panel/addresses/load_cities/${provinceId}`,
            type: 'get',
            success: function (response) {
                $('#id_city option:not(:first)').remove();
                $('#id_city').prop('disabled', false);
                for (var item of response.cities) {
                    $('#id_city').append(`<option value="${item.id}">${item.title}</option>`);
                }
            },
            error: function () {
                Swal.fire({
                    title: "خطا",
                    text: "عملیات با خطا مواجه شد لطفا مجدد تلاش کنید .",
                    icon: "error",
                    confirmButtonText: "باشه",
                });
            }
        });
    } else {
        $("#id_city option:not(:first)").remove();
        $("#id_city").prop("disabled", true);
    }
});

function delete_address() {
    Swal.fire({
        text: "آیا از انجام این عملیات مطمئن هستید؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "بله",
        cancelButtonText: "خیر"
    }).then((result) => {
        if (result.isConfirmed) {
            $('#address_form').submit();
        }
    });
}

function activate_address() {
    Swal.fire({
        text: "آیا از انجام این عملیات مطمئن هستید؟",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "بله",
        cancelButtonText: "خیر"
    }).then((result) => {
        if (result.isConfirmed) {
            $('#address_form_2').submit();
        }
    });
}