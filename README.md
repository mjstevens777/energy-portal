# energy-portal
CS194 Final Project

## Database

We have postgres instance set up at `stantron2.stanford.edu`.

### Connecting

To log, install psql and run

```sh
psql -d energy_portal -U energy_portal -h stantron2.stanford.edu
```

Add the following line to the file `$HOME/.pgpass`, where `*****` is the
password.

```
stantron2.stanford.edu:5432:energy_portal:energy_portal:*********
```

### Conventions

Use snake case (lower case with underscores) for everything in the database.

Make field names that are unique to a dataset globally unique, and
use the same name everywhere for foreign keys so that we can easily do
natural joins without any headaches.
