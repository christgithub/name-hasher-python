# name-hasher-python
ETL pipeline hashing strings and indexing result in MySQL

To build and bring the containers up
```
make up
```

To run the program
```
make run
```

After the program has run, at the prompt type:
```
make mysql
```

This will open a prompt in the running MySQL container

Enter 
```
select * from file_hashes limit 10;
```
A similar output is displayed, showing the first 10 rows of hashed names and and their source file

```
mysql> select * from file_hashes limit 10;
+----+----------------------+------------------------------------------------------------------+
| id | filename             | hash_value                                                       |
+----+----------------------+------------------------------------------------------------------+
|  1 | downloads/input2.txt | c4f7c543eee9e819960d769bf352a3f4a2429e165619139735ebe245d137c7e5 |
|  2 | downloads/input2.txt | 1314625ebeaf5b16b93f818fa941d696e5fa4719f4be0bb5b8e523904e5a5e56 |
|  3 | downloads/input2.txt | 33c1eed8d024575c87af4d6bdace5e0100d7d2bd0391569eeba4bf683c747fb5 |
|  4 | downloads/input2.txt | b128557d1fbf83b7031de1de48f410d8b9ee1f89398cda8cc8af912fd7569d69 |
|  5 | downloads/input2.txt | 9e2d43f55514924202ce4c6d3961149f5c4e3e726c583bdcd7cab2c77fd8f5c5 |
|  6 | downloads/input2.txt | c3f3869c8d9b2946adfce4fb3bce7fc9fb2e9110b2747b334bd8405cb7d4094d |
|  7 | downloads/input2.txt | 70b39cec82cb980a6c1adbc4b74fffac4707f1b5a1909bd598320e43a608af03 |
|  8 | downloads/input2.txt | fc9651de5bc42d3127d7a44806c34d87b27efc2d62b73c7a32d8d7a39ee0d624 |
|  9 | downloads/input2.txt | 823f3328d9ba489078624c15332232dc43ef56f508b6c79ea3437c596fec7379 |
| 10 | downloads/input2.txt | 8f67993675868c162fb62c38b1771ead36bfdae544fa540cf13f22a75bdeaa75 |
+----+----------------------+------------------------------------------------------------------+
10 rows in set (0.00 sec)
```
  


