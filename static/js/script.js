var generation_mode = 'random';
var password_string = 'empty';

var is_cluster_separation = false;
var is_length_increase = false;

var length = 8;
var default_length = 8;

var flags = [20, 0, 10, 0];
var default_flags = [20, 0, 10, 0];

var is_mode_selected = false;

function on_checker_box_length_increase()
{   
    if (is_length_increase)
    {
        // disabling increase
        is_length_increase = false;
        if (document.getElementById('slider_length').value > 20)
        {
            document.getElementById('slider_length').value = 20;
            document.getElementById('length_value').innerText = 20;
            on_slider(-1);
        }
        document.getElementById('slider_length').max = 20;
        default_length = 8;
        document.getElementById('length_increase_checkbox').checked = false;

    }
    else
    {
        // enabling increase
        is_length_increase = true;
        document.getElementById('slider_length').max = 60;
        default_length = 16;
    }
}

function on_checker_box_cluster_sep()
{
    if (is_cluster_separation)
    {
        // disabling separation
        is_cluster_separation = false
        document.getElementById('cluster_separation_checkbox').checked = false;
    }
    else
    {
        // enabling separation
        is_cluster_separation = true;
    }
}

function reset_sliders()
{
    document.getElementById('weight_lowercase_value').innerText = default_flags[0];
    document.getElementById('lowercase_slider').value = default_flags[0];
    
    document.getElementById('weight_uppercase_value').innerText = default_flags[1];
    document.getElementById('uppercase_slider').value = default_flags[1];
    
    document.getElementById('weight_numbers_value').innerText = default_flags[2];
    document.getElementById('numbers_slider').value = default_flags[2];

    document.getElementById('weight_punctuation_value').innerText = default_flags[3];
    document.getElementById('punctuation_slider').value = default_flags[3];
}


function on_slider(number)
{
    switch(number)
    {
        // length slider
        case -1:
            length = document.getElementById('slider_length').value;
            document.getElementById('length_value').innerText = length;
            break;
        
        // lowercase slider
        case 0:
            flags[0] = document.getElementById('lowercase_slider').value;
            document.getElementById('weight_lowercase_value').innerText = flags[0];
            break;

        // uppercase slider
        case 1:
            flags[1] = document.getElementById('uppercase_slider').value;
            document.getElementById('weight_uppercase_value').innerText = flags[1];
            break;

        // numbers slider
        case 2:
            flags[2] = document.getElementById('numbers_slider').value;
            document.getElementById('weight_numbers_value').innerText = flags[2];
            break;

        // punctuation slider
        case 3:
            flags[3] = document.getElementById('punctuation_slider').value;
            document.getElementById('weight_punctuation_value').innerText = flags[3];
            break;

        default:
            // do nothing
    }
    generate_string();
}

function generate_string()
{
    if (!is_mode_selected)
    {
        is_mode_selected = true;
        set_generation_mode(generation_mode);
        return;
    }

    fetch('/generate',
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            length: length,
            flags_lo: flags[0],
            flags_up: flags[1],
            flags_nu: flags[2],
            flags_pt: flags[3],
            generation_mode: generation_mode,
            is_cluster_separation: is_cluster_separation
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('generated_string_output').innerText = data.result_string;
    });

    document.getElementById('copy_button').disabled = false;
    document.getElementById('reset_button').disabled = false;
}

function set_generation_mode(mode)
{
    if (mode == 'random')
    {
        // mode to random
        generation_mode = mode;
        document.getElementById('btn_mode_random').disabled = true;
        document.getElementById('btn_mode_redable').disabled = false;
        document.getElementById('cluster_separation_checkbox').disabled = true;
        generate_string();
    }
    else if (mode == 'readable')
    {
        // mode to redable
        generation_mode = mode;
        document.getElementById('btn_mode_redable').disabled = true;
        document.getElementById('btn_mode_random').disabled = false;
        document.getElementById('cluster_separation_checkbox').disabled = false;
        generate_string();  
    }
}

function copy()
{
    let string_value = document.getElementById('generated_string_output').innerText;
    navigator.clipboard.writeText(string_value);
    document.getElementById('copy_button').disabled = true;
}

function reset()
{
    reset_sliders();
    document.getElementById('generated_string_output').innerText = "resetted"
    document.getElementById('slider_length').value = default_length;
    document.getElementById('length_value').innerText = default_length;
    length = default_length;
    
    flags = default_flags;
    
    if (is_length_increase)
    {
        on_checker_box_length_increase();
    }
        
    if (is_cluster_separation)
    {
        on_checker_box_cluster_sep();
    }
        
    document.getElementById('reset_button').disabled = true;
    document.getElementById('copy_button').disabled = false;        
}
