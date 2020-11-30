# h3map - Heroes of Might and Magic III map searcher

Searching for maps in Heroes III is extremely annoying given that you can only filter based on the map size. If you have a lot of maps it becomes very tedious to find maps matching you criteria. For example let's say you'd like to play a map with the following properties: 
- Two human players against any number of AI enemies
- Map size of XL
- Winning condition: all enemy heroes have no castle for 7 days
- You want to play either Castle or Dungeon

h3map should help you by reading all your .h3m maps and filtering them based on your own predefined criteria. This is still very early WIP, I will provide a list with possible search criteria once I have figured out the whole map header.

Additional features:
- Caching/Indexing map headers in a database (would be cool as reading the maps through the filesystem is slow)
- Memorizing what maps you have played, maybe with an additional score so that you can remember if you liked the map.
- Exporting/Importing the cache