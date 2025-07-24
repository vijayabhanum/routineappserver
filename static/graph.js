

$(document).ready(function(e){

    
    $('#submit').on('click', function(event){
        event.preventDefault();
        const year = $('#year').val();
        const month = $('#month').val();
        const type = $('#type').val();

        console.log(year, month, type);

        const given_input = [year, month, type];
        input = JSON.stringify(given_input);

        form_data = new FormData();
        form_data.append("input", input)

        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        headers = {
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        };

        $.ajax({
            url: '/graph_ajax/',
            type: 'POST',
            dataType: 'json',
            cache: false,
            headers: headers,
            data: form_data,
            contentType: false,
            processData: false,
            success:function(data){
                console.log("success");
                parsed = JSON.parse(data);
                image = parsed['img']
                image_data = 'data:image/png;base64,' + image;
                $('#graph_image').attr("src", image_data);
                $('#graph_image').removeClass('d-none');
            },
            error:function(data){
                console.log("error");
            },
        });

    })



})