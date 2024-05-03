function summonPokemon(event) {
    event.stopPropagation();


    const randomId = Math.floor(Math.random() * 151) + 1;
    fetch(`https://pokeapi.co/api/v2/pokemon/${randomId}`)
        .then(response => response.json())
        .then(data => {
            const pokemonName = data.name;
            const pokemonImage = data.sprites.front_default;
            document.getElementById('pokemonName').textContent = `You got ${pokemonName}!`;
            document.getElementById('pokemonImage').src = pokemonImage;
            document.getElementById('pokemonImage').alt = pokemonName;
            showModal();
        })
        .catch(error => {
            alert('Failed to retrieve Pokémon data.');
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
