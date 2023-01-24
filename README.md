# Genetic algorithm for decoding a text
The purpose of encryption is to convert the raw text (message) into ciphertext so that no one but the recipient of the message can understand it. 

The encryption used in this project is done using an encryption key and a table.<br>
The table can be seen here:

![](./table.jpg)

For this purpose, first a desired encryption key is selected. Then a new string is created using this key, and finally, using the Vigenère cipher table, the encrypted text is created. To start the encryption process, first a desired key is selected. This key will be repeated until it equals the text we want to encrypt in length. For example, if the text we want to encrypt is:

“WE ARE DISCOVERED SAVE YOURSELF”

and the key is "RUN,"  the initial string created will be:

"RU NRU NRUNRUNRUN RUNR UNRUNRUN" 

Finally, we will use the Vigenère cipher table to encrypt the text.



