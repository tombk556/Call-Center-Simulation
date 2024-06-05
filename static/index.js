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
                    <p>Customers Handled: ${response.customer_handled}</p>
                    <p>Impatient Customers: ${response.impatient_customers}</p>
                `);
            }
        });
    });
});