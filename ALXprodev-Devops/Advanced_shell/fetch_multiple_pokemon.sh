#!/bin/bash

# Step 1: Create a folder to store the results
mkdir -p pokemon_data

# Step 2: List of Pokémon
pokemon_list=("bulbasaur" "ivysaur" "venusaur" "charmander" "charmeleon")

# Step 3: Loop through each Pokémon
for pokemon in "${pokemon_list[@]}"
do
    echo "Fetching data for $pokemon..."
    
    curl -s "https://pokeapi.co/api/v2/pokemon/$pokemon" -o "pokemon_data/${pokemon}.json"
    
    if [ $? -eq 0 ]; then
        echo "Saved data to pokemon_data/${pokemon}.json ✅"
    else
        echo "Failed to fetch $pokemon ❌"
    fi
    
    sleep 2  # delay to avoid hitting API too fast
done

