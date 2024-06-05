$(document).ready(function() {
    $('#simulation-form').submit(function(event) {
        event.preventDefault();
        
        let numEmployees = parseInt($('#numEmployees').val());
        let avgSupportTime = parseInt($('#avgSupportTime').val());
        let customerInterval = parseInt($('#customerInterval').val());
        let simTime = parseInt($('#simTime').val());
        let patience = $('#patience').val().split('-').map(Number);

        $.ajax({
            url: '/submit',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                num_employees: numEmployees,
                avg_support_time: avgSupportTime,
                customer_interval: customerInterval,
                sim_time: simTime,
                patience: patience
            }),
            success: function(response) {
                $('#results').html(`
                    <div class="notification ">
                        <p class="is-size-6 has-text-weight-bold">Bediente Kunden: ${response.customer_handled}</p>
                        <p class="is-size-6 has-text-weight-bold">Abgesprungen Kunden: ${response.impatient_customers}</p>
                    </div>
                `);
            }
        });
    });
});