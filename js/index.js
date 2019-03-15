const express = require('express');
const _ = require('lodash');

const app = express();
const port = 4000;

const levelData = {
  zip3: require('./zip3.json'),
  // zip5: require('./zip5.json'),
};

app.get('/:level/:id', (req, res) => {
  const { level, id } = req.params;
  const data = levelData[level];
  let { features: polygonData } = data;

  switch(level.toLowerCase()) {
    case 'zip3':
      polygonData = polygonData.filter(p => _.get(p, ['properties', 'STATE']) === id);
      break;

    case 'zip5':
      polygonData = polygonData.filter(p => _.get(p, ['properties', 'ZIP']).startsWith(id));
      break;

    default:
      polygonData = [];
  }

  if (polygonData.length === 0) {
    return res.sendStatus(404);
  }

  polygonData = polygonData.map(itemData => {
      const id = itemData.properties[level.toUpperCase()];
      const { type } = itemData.geometry;
      let { coordinates: polygons } = itemData.geometry;

      if (type === 'Polygon') {
        polygons = [polygons];
      }

      polygons = polygons.map(points => {
        return _.get(points, 0, []).map(point => ({
          lat: point[1],
          lng: point[0],
        }));
      });

      return { id, polygons };
    });

  return res.send(polygonData);

});

app.listen(port, () => console.log(`App listening on port ${port}.`));
