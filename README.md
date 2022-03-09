# Verificacion de archivos:
Programa que se ejecuta mediante línea de comandos y contiene varias pruebas distintas para ejecutar:
* Test 1: Abrir archivos
  
  Esta prueba recibe un path de un directorio o un archivo y abrirá y cerrará todos los archivos dentro de este path. Tomará el tiempo de ejecución de la prueba y el tiempo total y generará un archivo de logs con estos tiempos.
  
* Test 2: Remover etiquetas HTML

  Esta prueba recibe un path de un directorio o un archivo HTML y removerá todas las etiquetas HTML (<>) de estos archivos. Generará un archivo de salida con el mismo contenido pero sin estas etiquetas (clean-nombre-original). Se tomará el tiempo de ejecución por archivo y el tiempo total y se generará un archivo de logs con estos tiempos.

* Test 3: Acomodar las palabras en un archivo

  Esta prueba recibe un path de un directorio o un archivo y acomodará todas las palabras por orden alfabético. Tiene la opción de eliminar caracteres especiales y dejar exclusivamente letras y números. Generará un archivo de salida con el mismo contenido pero con las palabras ordenadas (nombre-original-sorted). Se tomará el tiempo de ejecución por archivo y el tiempo total y se generará un archivo de logs con estos tiempos.
  

Se ejecuta mediante línea de comandos mandando a llamar al "main.py" y se le pueden pasar los siguientes parámetros para modificar la prueba:
*  -c , --cleanChars: Indica si se eliminaran caracteres especiales en las pruebas. Default: True
*  -e , --execTest: Test a ejecutar: "1" para Abrir archivos."2" para remover etiquetas HTML. "3" para acomodar las letras de un archivo."all" para ejecutar todas las pruebas. Default: all
*  -f , --fileType: Extension de los archivos a manipular al buscar en un directorio. Default: .html
*  -s , --sortedLogsDir: Directorio para los logs de la prueba 3. Default: path en donde se ejecute + "logs\sorted"
*  -o , --outputDir: Directorio en donde se guardaran los logs generados. Default: path en donde se ejecute + "logs"
*  -t , --cleanTagsDir: Directorio para los logs de la prueba 2.Default: path en donde se ejecute + "logs\clean_html"
*  -r , --rootDir: Directorio/archivo en donde se ejecutara la herramienta. Default: path en donde se ejecute el script.
