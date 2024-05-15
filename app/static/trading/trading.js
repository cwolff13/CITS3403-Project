let currentPokemonToReceive = '';
let currentPokemonToTradeOut = '';
var currentTradeId = null;

function openTradeModal() {
    document.getElementById('tradeModal').style.display = 'block';
}

function closeTradeModal() {
    document.getElementById('tradeModal').style.display = 'none';
}

function openTradeConfirmation(pokemonName, userName) {
    document.getElementById('tradeModal').style.display = 'block';
    document.getElementById('tradeModal').scrollIntoView();
    showPokemonToReceive();
    showPokemonToTradeOut();
    highlightPokemon('pokemonToReceiveList', pokemonName);
}

function highlightPokemon(listId, pokemonName) {
    const pokemonBoxes = document.querySelectorAll(`#${listId} .pokemon-box`);
    for (let box of pokemonBoxes) {
        if (box.querySelector('.pokemon-name').textContent === pokemonName) {
            box.style.border = '2px solid #007bff';
        } else {
            box.style.border = '1px solid #ddd';
        }
    }
}

function selectPokemonToReceive(pokemonName) {
    currentPokemonToReceive = pokemonName;
    highlightPokemon('pokemonToReceiveList', pokemonName);
}

function selectPokemonToTradeOut(pokemonName) {
    currentPokemonToTradeOut = pokemonName;
    highlightPokemon('pokemonToTradeOutList', pokemonName);
}

function confirmTrade() {
    if (currentPokemonToReceive && currentPokemonToTradeOut) {
        document.getElementById('selectedPokemonToReceive').textContent = currentPokemonToReceive;
        document.getElementById('selectedPokemonToTradeOut').textContent = currentPokemonToTradeOut;
        document.getElementById('confirmPopup').style.display = 'block';
    } else {
        alert('Please select both Pokemon to trade.');
    }
}

function confirmTradeFinal() {
    if (currentPokemonToReceive && currentPokemonToTradeOut) {
        // Send an AJAX request to Flask backend
        closeConfirmationModal();
        closeTradeModal();
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
            // Handle success response from Flask backend
            console.log(data);
            // Reset the current selections and close the modal
            currentPokemonToReceive = '';
            currentPokemonToTradeOut = '';
            
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
        window.location.reload()
    } else {
        alert('Please select both Pokémon to trade.');
    }
}

function closeConfirmationModal() {
    document.getElementById('confirmPopup').style.display = 'none';
}

function confirmAvailableTrade(tradeId) {
    // Store the trade ID and show the confirmation modal
    currentTradeId = tradeId;
    document.getElementById('confirm-available-trade').style.display = 'block';
}
function confirmAvailableTradeFinal() {
    if (currentTradeId) {
        // Send an AJAX request to delete the trade
        fetch('/trading?trade_id=' + currentTradeId, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                // If successful, reload the page to reflect changes
                window.location.reload();
            } else {
                // Handle errors
                console.error('Failed to delete trade');
            }
        })
        .catch(error => {
            // Handle network errors
            console.error('Error:', error);
        });
        // Close the confirmation modal
        closeAvalableTradeConfirmation();
        // Reset the current trade ID
        currentTradeId = null;
        window.location.reload()
    } else {
        // If no trade ID is selected, show an alert
        alert('Please select a trade.');
    }
}

function closeAvalableTradeConfirmation() {
    // Close the confirmation modal
    document.getElementById('confirm-available-trade').style.display = 'none';
}