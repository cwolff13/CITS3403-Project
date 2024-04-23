function summonPokemon() {
    var pokemonId = Math.floor(Math.random() * 151) + 1;
    alert("You caught Pokémon ID: " + pokemonId); //Currently returns a Alert with pokemon ID, in future will pull from API and return JSON object for caught pokemon. 
}
