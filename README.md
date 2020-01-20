ViBE
====

This app will determine the chord progression to a piece of music (using standard Western harmony) just by listening to it. It's basically Shazam but for chords.

The app implements a pitch detection algorithm in Python that isolates individual pitches. Currently, a neural network model is being trained both to improve the pitch detection accuracy and to assemble the pitches into coherent chord progressions.