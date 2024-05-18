// Initialize variables to store the selected Pokémon names and trade ID
let currentPokemonToReceive = '';
let currentPokemonToTradeOut = '';
var currentTradeId = null;

// Function to open the trade modal
function openTradeModal() {
    document.getElementById('tradeModal').style.display = 'block';
}

// Function to close the trade modal
function closeTradeModal() {
    document.getElementById('tradeModal').style.display = 'none';
}

// Function to highlight the selected Pokémon for trading in and out
function highlightPokemon(listId, pokemonName) {
    const pokemonBoxes = document.querySelectorAll(`#${listId} .pokemon-box`);
    for (let box of pokemonBoxes) {
        if (box.querySelector('.pokemon-name').textContent === pokemonName) {
            box.style.border = '2px solid #007bff';     // Highlight the selected Pokémon
        } else {
            box.style.border = '1px solid #ddd';        // Reset the border for non-selected Pokémon
        }
    }
}

// Function to select a Pokémon to receive in the trade
function selectPokemonToReceive(pokemonName) {
    currentPokemonToReceive = pokemonName;                      // Update the selected Pokémon to receive
    highlightPokemon('pokemonToReceiveList', pokemonName);      // Highlight the selected Pokémon
}

// Function to select a Pokémon to trade out
function selectPokemonToTradeOut(pokemonName) {
    currentPokemonToTradeOut = pokemonName;                     // Update the selected Pokémon to trade out
    highlightPokemon('pokemonToTradeOutList', pokemonName);     // Highlight the selected Pokémon
}

// Function to open the confirmation popup for posting a trade
function confirmTrade() {
    if (currentPokemonToReceive && currentPokemonToTradeOut) {
        // Display the selected Pokémon in the confirmation popup
        document.getElementById('selectedPokemonToReceive').textContent = currentPokemonToReceive;
        document.getElementById('selectedPokemonToTradeOut').textContent = currentPokemonToTradeOut;
        document.getElementById('confirmPopup').style.display = 'block';
    } else {
        alert('Please select both Pokemon to trade.');  // Alert if either one is not selected
    }
}

// Function to handle the final confirmation of posting a trade using AJAX
function confirmTradeFinal() {
    if (currentPokemonToReceive && currentPokemonToTradeOut) {
        // Close the confirmation and trade modals
        closeConfirmationModal();
        closeTradeModal();

        // Prepare the form data for the AJAX request
        let formData = new FormData();
        formData.append('pokemon_to_receive', currentPokemonToReceive);
        formData.append('pokemon_to_trade_out', currentPokemonToTradeOut);
        fetch('/trading', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            // Handle the success response from the Flask backend
            console.log(data);
            // Reset the current selections and close the modal
            currentPokemonToReceive = '';
            currentPokemonToTradeOut = '';
            alert(data.message);        // Display flash message to the user
            window.location.reload();   // Reload the page to reflect changes
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
    } else {
        alert('Please select both Pokémon to trade.');  // Alert if either one is not selected
    }
}

// Function to close the confirmation popup
function closeConfirmationModal() {
    document.getElementById('confirmPopup').style.display = 'none';
}

// Function to open the available trade confirmation popup
function confirmAvailableTrade(tradeId) {
    currentTradeId = tradeId;                                                       // Store the trade ID
    document.getElementById('confirm-available-trade').style.display = 'block';     // Show the confirmation modal
}

// Function to handle the final confirmation of an available trade using AJAX
function confirmAvailableTradeFinal() {
    if (currentTradeId) {
        // Send an AJAX request to delete the trade
        fetch('/trading?trade_id=' + currentTradeId, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Failed to delete trade');
        })
        .then(data => {
            // Handle success response from Flask backend
            console.log(data);
            alert(data.message);         // Display flash message to the user
            window.location.reload();    // Reload the page to reflect changes
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
            alert('Failed to delete trade');    // Display an error message to the user
        });
        // Close the confirmation modal and reset the trade ID
        closeAvalableTradeConfirmation();
        currentTradeId = null;
    } else {
        alert('Please select a trade.');        // Alert if no trade is selected
    }
}

// Function to close the available trade confirmation popup
function closeAvalableTradeConfirmation() {
    document.getElementById('confirm-available-trade').style.display = 'none';
}