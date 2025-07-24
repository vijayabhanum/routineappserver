
$(document).ready(function(e){
    i=0
    
    function questions_ajax(){
        console.log("here in function!!");

        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        headers = {
            'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
        };

        const day = $('#day').text();
        const month = $('#month').text();
        const year = $('#year').text();

        console.log(day, month, year);

        form_data = new FormData();
        form_data.append('day', day);
        form_data.append('month', month);
        form_data.append('year', year);

        
        $.ajax({
            url: '/report_questions_ajax/',
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
                processdata(parsed);   
            },
            error:function(data){
                console.log("error");
            },
        });

    };
         

    questions_ajax();



    function processdata(parsed){
            lastProcess();
            
            $('#yes').on('click', function(event){
                event.preventDefault();
                parsed[i-1].push("yes");
                lastProcess();
                
            });
            $('#no').on('click',function(event){
                event.preventDefault();
                parsed[i-1].push("no");
                lastProcess();
                
            });

        function lastProcess(){
            parsed_length = parsed.length;
            console.log(parsed_length);
            if(i<parsed_length){
                routine_text = "Routine"+"   "+ parsed[i][0] +", "+ "Task" +"  " + parsed[i][1].toUpperCase();
                question_text = parsed[i][2];
                
                $('#routine').text(routine_text);
                $('#question').text(question_text);
                i = i + 1;
            }
            else{
                $("#question_card").addClass("d-none");
                $("#yes").prop("disabled", true);
                $("#yes").addClass("d-none");
                $("#no").prop("disabled", true);
                $("#no").addClass("d-none");
                $("#comment_row").removeClass("d-none");

                

                $("#submit_comment").on("click", function(){
                
                new_data = JSON.stringify(parsed);
                const day = $('#day').text();
                const month = $('#month').text();
                const year = $('#year').text();

                date = [year,month,day]
                new_date = JSON.stringify(date)

                const comment_js = $("#comment").val();
                
                comment = JSON.stringify(comment_js);
                
                console.log(comment_js)
                
                report_form = new FormData();
                report_form.append("date", new_date);
                report_form.append("parsed", new_data);
                report_form.append("comment", comment);

                csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
                headers = {
                    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
                    'X-CSRFToken': csrf_token,
                };

                $.ajax({
                    url: '/report_input_ajax/',
                    type: 'POST',
                    dataType: 'json',
                    cache: false,
                    headers: headers,
                    data: report_form,
                    contentType: false,
                    processData: false,
                    success:function(data){
                        console.log("success");
                        $("#comment_row").addClass("d-none");
                        $("#success_card").removeClass("d-none");
                        $("#done_data").text("Success... Redirecting in 3...2...1..");
                        setTimeout(function() {
                                const homebut = document.getElementById("homepage");
                                homebut.click();
                                }, 3000);
                    },
                    error:function(data){
                        console.log("error");
                        $("#comment_row").addClass("d-none");
                        $("#success_card").removeClass("d-none");
                        $("#done_data").text("Error");

                    },
                });

            });

        }
        };
     
        };


        document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowUp') {
           const yesbut = document.getElementById('yes');
           yesbut.click();
        }
        if (event.key === 'ArrowDown') {
            const nobut = document.getElementById('no');
            nobut.click();
        }
        });

});
