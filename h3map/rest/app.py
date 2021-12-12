import glob

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from h3map.library.library import Library
from h3map.discover.maps4heroes import DiscoverMaps4Heroes
from h3map.discover.remote_map_loader import UrlHtmlMapInfoLoader
from h3map.view.view import MapsView

app = Flask("h3map")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/aless/Games/HoMM 3 Complete/Maps/h3map.db'
db = SQLAlchemy(app)


class MapMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'summary': self.summary,
            'thumbnail': self.thumbnail,
        }


db.create_all()


@app.route("/scan")
def scan_library():
    controller = Library()
    exp = str("C:/Users/aless/Games/HoMM 3 Complete/Maps/*.h3m")
    maps_in_dir = glob.glob(exp)
    new_maps = []
    for path in maps_in_dir:
        if db.session.query(MapMetadata.id).filter_by(path=path).scalar() is None:
            new_maps.append(path)

    if not len(new_maps):
        return jsonify({
            "success": True
        })

    headers: MapsView = controller.load(new_maps).all()
    for header, path in zip(headers, new_maps):
        map_metadata_model = MapMetadata(name=header.metadata.description.name, summary=header.metadata.description.summary,
                                   thumbnail=header.metadata.thumbnail, path=path)
        db.session.add(map_metadata_model)

    db.session.commit()

    return jsonify({'success': True})


@app.route("/maps")
def maps():
    all_maps = MapMetadata.query.all()
    results = [header.format() for header in all_maps]
    return jsonify({
        'success': True,
        'results': results,
        'count': len(results),
    })


@app.route("/online-maps/<int:page>")
def online_maps(page=0):
    #discover = DiscoverMaps4Heroes(FileHtmlMapInfoLoader("C:/Users/aless/Projects/Homm3_Hota_Map_Searcher/h3map"
    #                                                     "/reference_maps/maps4heroes.html"))
    discover = DiscoverMaps4Heroes(UrlHtmlMapInfoLoader("https://www.maps4heroes.com/heroes3/maps.php"))
    results = []
    for header in discover.list_maps(page=page):
        results.append({
            'id': None,
            'name': header.metadata.description.name,
            'summary': header.metadata.description.summary,
            'thumbnail': header.metadata.thumbnail,
        })

    return jsonify({
        'success': True,
        'results': results,
        'count': len(results),
    })
