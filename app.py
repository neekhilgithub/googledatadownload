from flask import Flask, render_template, request
from samgeo import tms_to_geotiff

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    basemap_choice = request.form['basemap']
    bbox_input = request.form['bbox']
    output_filename = request.form.get('filename', 'output')

    try:
        bbox = [float(coord.strip()) for coord in bbox_input.split(',')]
    except ValueError:
        return "Invalid input! Please enter numeric values."

    try:
        tms_to_geotiff(output=output_filename + ".tif", bbox=bbox, zoom=19, source=basemap_choice, overwrite=True)
        return "Download successful! <a href='/'>Go back</a>"
    except Exception as e:
        return "Error: " + str(e) + " <a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)