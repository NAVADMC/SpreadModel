var results_status  = (function(pollTime){
    var pollInterval,
        last_progress = 1;

    var update_results_status = function() {
        $.get('/results/simulation_status.json').done(function (context) {
            if( context.is_simulation_stopped ){ //not running but has started means it is now stopped 
                stop_poll()
                window.location.reload();
                //return
            }
            if( context.simulation_has_started) {
                var simulation_complete = context.iterations_completed == context.iterations_total
                var simulation_progress = context.iterations_total === 0 ? 0 :
                        Math.max(context.iterations_completed / context.iterations_total,
                            0.5 / context.iterations_total)
                var status_text = context.iterations_completed + " of " + context.iterations_total + " iterations completed.";

                if (simulation_complete) {
                    $('.simulation-progress').addClass('done');
                    status_text = "Simulation complete.  " + context.iterations_total + " iterations run.";
                }
                $('.simulation-progress').width(simulation_progress * 100 + "%");

                var $iterationText = $('#iteration_text')[0];
                //check scroll position before changing anything
                var isScrolledToBottom = $iterationText.scrollHeight - $iterationText.clientHeight <= $iterationText.scrollTop + 10;// allow 10px inaccuracy
                $('#iteration_text').html(context.iteration_text) //insert the text
                if(isScrolledToBottom) //readjust the scroll
                    $iterationText.scrollTop = $iterationText.scrollHeight - $iterationText.clientHeight;
            }
            else {  //simulation hasn't started
                status_text = "Starting Simulation..."
            }
            $('.simulation-status').text(status_text);
            if(context.iterations_completed >= 1) {
                var abort_btn = document.getElementById("sim_abort_btn");
                abort_btn.classList.remove('hidden');
            }

            last_progress = simulation_progress;
        });
    },

        start_poll = function() { pollInterval = setInterval(update_results_status, pollTime); update_results_status(); },
        stop_poll = function() {
            clearInterval(pollInterval);
        };


    return {
        start_poll: start_poll,
        stop_poll: stop_poll,
        get_last_progress: function() { return last_progress; }
    };
})(3000);

results_status.start_poll();
