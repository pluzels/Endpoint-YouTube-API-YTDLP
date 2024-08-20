const { exec } = require('youtube-dl-exec');

module.exports = async (req, res) => {
  const link = req.query.links;

  if (!link) {
    return res.status(400).json({ error: 'Link parameter is required' });
  }

  try {
    const options = {
      format: 'bestaudio',
      output: '-'
    };

    const stream = exec(link, options);

    res.setHeader('Content-Disposition', 'attachment; filename="audio.mp3"');
    stream.stdout.pipe(res);
  } catch (error) {
    res.status(500).json({ error: 'Failed to download video' });
  }
};
