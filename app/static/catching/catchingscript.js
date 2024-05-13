function summonPokemon(event) {
    event.stopPropagation();
    const userId = 1; // Hard-coded user ID for testing

    fetch('/catching-pokemon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: userId  // Correctly structured JSON body
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const pokemonName = data.pokemon.name;
            const pokemonImage = data.pokemon.image;
            document.getElementById('pokemonName').textContent = `You got ${pokemonName}!`;
            document.getElementById('pokemonImage').src = "static/" + pokemonImage;
            document.getElementById('pokemonImage').alt = pokemonName;
            document.getElementById('pokeballcount').textContent = `Remaining Pokeballs: ${data.newPokeballCount}`;
            showModal();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        alert('Failed to communicate with the server.');
        console.error('Error:', error);
    });
}


function showModal() {
    const modal = document.getElementById('pokemonModal');
    const span = document.getElementsByClassName('close')[0];

    modal.style.display = "block";
    span.onclick = function() {
        modal.style.display = "none";
    };
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}
