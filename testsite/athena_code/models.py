import logging
import os
import subprocess

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse

logger = logging.getLogger(__name__)


class Repo(models.Model):
    """ Model representing the GH repo. """
    name = models.CharField(max_length=100, help_text='Enter the name for the repo',
                            default='')

    url = models.URLField(max_length=500, help_text='Enter the url for the GH repo',
                           default='')

    data = JSONField(blank=True, null=True, help_text=
                     'Enter any additional data about the as a dict')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this repo."""
        return reverse('repo-detail', args=[str(self.id)])


class Fork(models.Model):
    """ Model representing the fork of a github Repo. """
    name = models.CharField(max_length=100, help_text='Enter the name for the fork',
                            default='')

    url = models.URLField(max_length=500, help_text='Enter the url for the GH fork',
                           default='')

    data = JSONField(blank=True, null=True, help_text=
                     'Enter any additional data about the as a dict')

    code = models.OneToOneField('Code', help_text='Select a code for this fork',
                                on_delete=models.SET_NULL, null=True)

    # Here foreign key is used because a fork has one repo, but the repo can have many forks
    repo = models.ForeignKey('Repo', help_text='Select a repo for this fork',
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this fork."""
        return reverse('fork-detail', args=[str(self.id)])

    def get_clone_url(self):
        """ Returns the clone url to access after fork is cloned."""
        return reverse('fork-clone-detail', args=[str(self.id)])

    def get_configure_url(self):
        """ Returns the configuration url that will clone and configure a fork."""
        return reverse('configuration-create', args=[str(self.code.id)])


class Branch(models.Model):
    """ Model representing the branch of a github Fork or Repo. """
    name = models.CharField(max_length=100, help_text='Enter the name for the branch',
                            default='')
    
    # here foreign key is used because a branch has one fork, but a fork can have many branches
    fork = models.ForeignKey('Fork', help_text='Select a fork for this branch',
                             on_delete=models.SET_NULL, null=True)

    # Here foreign key is used because a fork has one repo, but the repo can have many forks
    repo = models.ForeignKey('Repo', help_text='Select a repo for this branch',
                             on_delete=models.SET_NULL, null=True)

    data = JSONField(blank=True, null=True, help_text=
                     'Enter any additional data about the as a dict')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this branch."""
        return reverse('branch-detail', args=[str(self.id)])


class Code(models.Model):
    """ Model representing the actual Athena Code, which exists on the local system. """

    # path for the code
    path = models.CharField(default=settings.BASE_DIR + '/mycode',
                            help_text='Select where to place this code.',
                            max_length=500)
    # name for the code
    name = models.CharField(help_text='Enter a name for this code.',
                            max_length=500)

    # this is a tricky variable, it is set when the code is configured, for that reason it is
    # similar to a property, maybe there is a better way to do this?
    configuration = None

    @property
    def cloned(self):
        return os.path.exists(self.path)

    @property
    def configurations(self):
        return self.configuration_set.all()

    @property
    def configured(self):
        return os.path.exists(self.path + '/Makefile')

    @property
    def compiled(self):
        return os.path.exists(self.path + '/bin/athena')

    def clone(self):
        """ Clone the repo/fork if it doesn't exist. """
        if not self.cloned:
            logger.info('Cloning the git repo from {}'.format(self.fork.url))
            os.system("mkdir {}".format(self.path))
            result = subprocess.check_output(["git", "clone", self.fork.url, self.path])
            if not result:
                result = 'success'
            logger.info('Result of the clone was: {}'.format(result))
        else:
            logger.info('{} is already cloned, ignoring'.format(self.name))

    def configure(self, **filter):
        """ Configure the athena code """
        query = self.configurations.filter(**filter)
        if query.count() > 1:
            logger.error('Got {}, which configuration do you want?'.format(query))
        else:
            # set the configuration
            self.configuration = query.last()
            logger.info('Configuring athena with {}'.format(self.configuration))
            self.configuration.configure()

    def compile(self, options='-j', **filter):
        """ Compile the athena code """
        if not self.configured:
            self.configure(**filter)
        command = ["make", options, "all"]
        try:
            logger.info('Compiling athena code with command {}'.format(command))
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=self.path,
                                             universal_newlines=True)
            logger.info("Compilation details: {}".format(result))
        except subprocess.CalledProcessError as e:
            logger.exception('{}/make hit an exception...'.format(
                self.name)
            )
            logger.error("Compilation failed with message\n: {}".format(e.output))

    def run(self, options='-i', **filter):
        if not self.compiled:
            self.compile(**filter)

        command = [
            "./athena",
            options,
            self.configuration.input_file
        ]
        try:
            logger.info("Running athena with command {}".format(command))
            result = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                             cwd=self.path+'/bin/',
                                             universal_newlines=True)
            logger.info("Run details: {}".format(result))
        except subprocess.CalledProcessError as e:
            logger.exception('{}/bin/athena hit an exception...'.format(
                self.name)
            )
            logger.error("Athena Run failed with message\n: {}".format(e.output))

    def clean(self):
        if self.configured:
            logger.info('Removing compiled files from {}'.format(self.name))
            os.system("cd {} && make clean".format(self.path))

    def remove(self):
        """ Delete the cloned repo if it exists. """
        if self.cloned:
            logger.info('Removing cloned repo {}'.format(self.name))
            os.system("rm -rf {}".format(self.path))
        if self.configured:
            # reset configuration
            logger.info('Resetting configuration from {} to None'.format(self.configuration))
            self.configuration = None

    def list_problems(self):
        self.clone()
        logger.info('Listing all problems...')
        return os.listdir(self.path + '/src/pgen')

    def list_input_files(self):
        self.clone()
        logger.info('Getting all input files...')
        return [
            os.path.join(dp, f) for dp, dn, fn in os.walk(
                os.path.expanduser(self.path + '/inputs')
            ) for f in fn
        ]

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this branch."""
        return reverse('code-detail', args=[str(self.id)])

    def get_configure_url(self):
        """ Returns the configuration url that will clone and configure this code. """
        return reverse('configuration-create')

    def get_clone_url(self):
        """ Returns the clone url to access after code is cloned."""
        return reverse('code-clone-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Configuration(models.Model):
    """ Model representing a configuration of the Athena Code. """
    HDF5_SERIAL_PATH = "/usr/include/hdf5/serial/"
    HDF5_PARALLEL_PATH = "/usr/include/hdf5/openmpi/"

    # a configuration is associated with code
    code = models.ForeignKey('Code', help_text='Select code for this configuration',
                             on_delete=models.SET_NULL, null=True)

    input_file = models.CharField(help_text='Enter the input file for this configuration.',
                                  max_length=500, default='', blank=True)

    input_dict = JSONField(blank=True, null=True,
                           help_text="Enter the input file for this problem as a dictionary."
                                     "The root keys should be the blocks of the input_file.")

    # the following are for each of the configuration fields
    prob = models.CharField(help_text='Select a problem to configure',
                            max_length=100, default='blast')

    coords = models.CharField(help_text='Select a coordinate system',
                              choices=(
                                  ('cartesian', 'Cartesian'),
                                  ('cylindrical', 'Cylindrical'),
                                  ('spherical_polar', 'Spherical Polar'),
                                  ('minkowski', 'Minkowski'),
                                  ('sinusoidal', 'Sinusoidal'),
                                  ('tilted', 'Tilted'),
                                  ('schwarzschild', 'Schwarzchild Metric'),
                                  ('kerr-schild', 'Kerr-Schild Metric'),
                                  ('gr_user', 'GR User Metric')
                              ), default='cartesian', max_length=100)

    eos = models.CharField(help_text='Select an equation of state',
                           choices=(
                               ('adiabatic', 'Adiabatic'),
                               ('Isothermal', 'Isothermal')
                           ), default='adiabatic', max_length=100)

    flux = models.CharField(help_text='Select Riemann solver',
                            choices=(
                                ('default', 'Default (depends on other fields)'),
                                ('hlle', 'Hartan, Lax, van Leer, Einfeldt (HLLE)'),
                                ('hllc', 'Hartan, Lax, van Leer, Contact (HLLC)'),
                                ('hlld', 'Hartan, Lax, van Leer, Discontinuities (HLLD)'),
                                ('roe', 'Roe Solver'),
                                ('llf', 'LLF Solver'),
                            ), default='default', max_length=100)

    fluxcl = models.CharField(help_text='Select Riemann solver for the collisionless variables',
                              choices=(
                                  ('hlle', 'Hartan, Lax, van Leer, Einfeldt (HLLE)'),
                                  ('roe', 'Roe Solver'),
                              ), default='roe', max_length=100)

    grav = models.CharField(help_text='Select a self-gravity solver.',
                            choices=(
                                ('none', 'No self-gravity'),
                                ('fft', 'Fast Fourier Transform'),
                                ('fft_cyl', 'Fast Fourier Transform in Cylindrical Coords')
                            ), default='none', max_length=100)

    nscalars = models.IntegerField(help_text='Enter number of scalars',
                                   default=0)

    nghost = models.IntegerField(help_text='Enter the number of ghost zones',
                                 default=2)

    bfield = models.BooleanField(help_text='Enable magnetic fields?',
                                 default=False)

    cless = models.BooleanField(help_text='Enable collisionless solver?',
                                default=False)

    cless_only = models.BooleanField(help_text='Enable collisionless-only mode?',
                                     default=False)

    spec_rel = models.BooleanField(help_text='Enable special relativity?',
                                   default=False)

    gen_rel = models.BooleanField(help_text='Enable general relativity?',
                                  default=False)

    transforms = models.BooleanField(help_text='Enable interface frame transformations for GR?',
                                     default=False)

    shear = models.BooleanField(help_text='Enable shearing box?',
                                default=False)

    dual_energy = models.BooleanField(help_text='Enable dual energy?',
                                      default=False)

    debug = models.BooleanField(help_text='Enable debug mode?',
                                default=False)

    float_precision = models.BooleanField(help_text='Enable single precision?',
                                          default=False)

    openmp = models.BooleanField(help_text='Enable parallelization with OpenMP?',
                                 default=False)

    mpi = models.BooleanField(help_text='Enable parallelization with MPI?',
                              default=False)

    fft = models.BooleanField(help_text='Enable fast fourier transform?',
                              default=False)

    fftw_path = models.CharField(help_text='Enter path to FFTW libraries',
                                 default='', max_length=100, blank=True)

    hdf5 = models.BooleanField(help_text='Enable HDF5 Output',
                               default=False)

    hdf5_path = models.CharField(help_text='Enter path to HDF5 libraries',
                                 default='', max_length=100, blank=True)

    cxx = models.CharField(help_text='Select C++ compiler',
                           choices=(
                               ('g++', 'g++'),
                               ('g++-simd', 'g++-simd'),
                               ('icc', 'icc-debug'),
                               ('cray', 'cray'),
                               ('bgxl', 'bgxl'),
                               ('icc-phi', 'icc-phi'),
                               ('clang++', 'clang++'),
                               ('clang++-simd', 'clang++-simd')
                           ), default='g++', max_length=100)

    ccmd = models.CharField(help_text='Override for command to used to call C++ compiler',
                            default='', max_length=100, blank=True)

    cflag = models.CharField(help_text='Addition str of flags to append to compiler/linker call',
                             default='', max_length=100, blank=True)

    include = models.CharField(help_text='use -Ipath when compiling',
                               default='', max_length=500, blank=True)

    lib = models.CharField(help_text='use -Lpath when linking',
                           default='', max_length=500, blank=True)

    def configure(self):
        """ Run the configuration code. """
        command = [
            "python",
            "configure.py",
            "--prob", self.prob,
            "--coord", self.coords,
            "--eos", self.eos,
            "--flux", self.flux,
            "--fluxcl", self.fluxcl,
            "--nghost={}".format(self.nghost),
            "--ns={}".format(self.nscalars),
            "--grav={}".format(self.grav),
            "--cxx={}".format(self.cxx)
        ]
        command = self._parse_args(command)
        if not self.code.cloned:
            self.code.clone()
        # run the configuration command
        logger.info("Configuring {} with command {}".format(self.code.name, command))
        try:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=self.code.path,
                                             universal_newlines=True)
            logger.info("Configuration details: {}".format(result))
        except subprocess.CalledProcessError as e:
            logger.exception('{}/configure.py hit an exception...'.format(
                self.code.name)
            )
            logger.error("Configuration failed with message\n: {}".format(e.output))
        return self

    def _parse_args(self, cmd):
        """ Append any additional args to command list """
        if self.bfield:
            cmd.append("-b")
        if self.cless:
            cmd.append("-cl")
        if self.cless_only:
            cmd.append("-clo")
        if self.spec_rel:
            cmd.append("-s")
        if self.gen_rel:
            cmd.append("-g")
        if self.transforms:
            cmd.append("-t")
        if self.shear:
            cmd.append("-shear")
        if self.dual_energy:
            cmd.append("-de")
        if self.debug:
            cmd.append("-debug")
        if self.float_precision:
            cmd.append("-float")
        if self.mpi:
            cmd.append("-mpi")
        if self.openmp:
            cmd.append("-omp")
        if self.hdf5:
            cmd.append("-hdf5")
            # TODO: think of better way to handle hdf5, since it will be necessary for the
            #       plotter
            if self.mpi:
                if not self.include:
                    self.include = self.HDF5_PARALLEL_PATH
            else:
                if not self.include:
                    self.include = self.HDF5_SERIAL_PATH
        if self.fft:
            cmd.append("-fft")
        if self.hdf5_path:
            cmd.append("--hdf5_path={}".format(self.hdf5_path))
        if self.fftw_path:
            cmd.append("--fftw_path={}".format(self.fftw_path))
        if self.ccmd:
            cmd.append("--ccmd={}".format(self.ccmd))
        if self.cflag:
            cmd.append("--cflag={}".format(self.cflag))
        if self.include:
            cmd.append("--include={}".format(self.include))
        if self.lib:
            cmd.append("--lib={}".format(self.lib))

        return cmd

    def _link_hdf5_lib(self):
        # TODO, think of way to implement this? Maybe this will be for dockerized version
        # if self.mpi:
        # run command: sudo ln -s /usr/lib/x86_64-linux-gnu/libhdf5_openmpi.so
        #                         /usr/lib/x86_64-linux-gnu/libhdf5.so
        # else:
        # run command: sudo ln -s /usr/lib/x86_64-linux-gnu/libhdf5_serial.so
        #                         /usr/lib/x86_64-linux-gnu/libhdf5.so
        pass

    def _read_input(self):
        """ This function will read the input file into a dictionary. """
        logger.info('Reading input file: {} into a dictionary ...'.format(self.input_file))
        input_dict = {}
        if not self.input_file:
            logger.error("Input file has not been set, there is nothing to read here!")
            raise Exception("Input file has not been set, there is nothing to read!")
        with open(self.input_file) as f:
            data = f.read().splitlines()
            blocks = []
            for i, line in enumerate(data):
                if "<" in line:
                    blocks.append((i, line))
            for i in range(len(blocks)):
                name = blocks[i][1]
                # get start, end indices of the block data
                start = blocks[i][0] + 1
                try:
                    end = blocks[i+1][0] - 1
                except IndexError:
                    end = None
                block_dict = {}
                for x in data[start:end]:
                    split = x.split("=")
                    try:
                        key, value = split[0].strip(), split[1].strip().replace("\t", " ")
                        block_dict[key] = value
                    except IndexError:
                        pass
                input_dict[name] = block_dict
        # set the input dict after reading the file
        self.input_dict = input_dict

    def _write_input(self, path='', name=''):
        """ This function will write the input dictionary to a file. """
        if not self.input_dict:
            logger.error("Input dictionary is empty! Nothing to write.")
            raise Exception("Input dictionary is empty! Nothing to write.")
        path = self.code.path + '/' if not path else path
        name = 'athinput.{}'.format(self.prob) if not name else name
        logger.info("Writing input file from input dict to {} with name {}".format(path, name))

        with open(self.input_file, 'w+') as f:
            for key in self.input_dict.keys():
                f.write("{}\n".format(key))
                for k, v in self.input_dict[key].items():
                    f.write("{} = {}\n".format(k, v))

        # Set the new input file name
        self.input_file = path + name

    def get_absolute_url(self):
        """ Returns the url to access a detail record for this branch."""
        return reverse('configuration-detail', args=[str(self.id)])

    def get_update_url(self):
        """ Returns the url to access a detail record for this branch."""
        return reverse('configuration-update', args=[str(self.id)])

    def __str__(self):
        return "{}-id{}".format(self.prob, self.id)
