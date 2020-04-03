# information-theory

This is my project for Information Theory course 88-782. <br>
The new compression is called `Rotem Compression` or `rg compression` (my initials).

It utilize 4 methods, described in the attached PDF file:
<ol>
<li>Lempel-Ziv-Welch method  (the method in active use here)</li>
<li>Huffman method</li>
<li>Lempel-Ziv-Welch method + Huffman for encoding the results</li>
<li>"Words Encoding" - using Huffman method to encode words instead of singular symbols</li>
</ol>


<h2>Project Structure</h2>
<pre>
├── README.md               // YOU ARE HERE
├── setup.py                // standard python setup file
├── app.py                  // main file for the package, applying the compression on user input
├── rgcompress              // bash file initiating the pyton app.py
├── test                    
|   └──                     // contains demos for input file, zip compression and rg compression
└── rotem_compressor
    ├── contract
    │   └── ...             // python interfaces for the compression methods
    ├── data_models
    │   └── ...             // data models used by the compression methods
    ├── huffman_compression
    │   └── ...
    ├── lzw.py
    ├── words_encoder.py
    ├── utils.py            // utilities used by the the compression methods 
    ├── rotem_compressor.py // the main compressor, applying multiple compressions on top of each other
    └── unittests
        └── ...             // unittests for the entire project 

</pre>

<h2>Usage:</h2>

<b>for compression:</b>
`rgcompress -i <inputFile> -o <outputFile>`<br>
or `python app.py -i <inputFile> -o <outputFile>`


<b>for decompression:</b> 
 `rgcompress -d -i <inputFile> -o <outputFile>`<br>
or `python app.py -d -i <inputFile> -o <outputFile>`
