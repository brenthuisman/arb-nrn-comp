import glia, glia.library
import arbor
from patch import p


class AllProperties:
    def __init__(self, neuron_base=True, v_init=-65, K=305.15, rL=35.4, cm=0.01, **kwargs):
        if neuron_base:
            self._props = arbor.neuron_cable_properties()
        else:
            self._props = arbor.cable_global_properties()
        self._props.set_property(Vm=v_init, tempK=K, rL=rL, cm=cm)
        grouped_by_ion = {}
        for k, v in kwargs.items():
            parts = k.split("_")
            ion = parts[0]
            prop = "_".join(parts[1:])
            ion_props = grouped_by_ion.setdefault(ion, dict())
            ion_props[prop] = v
        print(grouped_by_ion)
        for ion, props in grouped_by_ion.items():
            print("setting", ion, props)
            self._props.set_ion(ion=ion, **props)

    @property
    def properties(self):
        return self._props

def make_props(**kwargs):
    default = dict(
        na_int_con=10.0, na_ext_con=140.0, na_rev_pot=50.0,
        k_int_con=54.4, k_ext_con=2.5, k_rev_pot=-77.0,
        ca_int_con=0.00005, ca_ext_con=2.0, ca_rev_pot=132.5,
        cal_int_con=0.00005, cal_ext_con=2.0, cal_rev_pot=132.5, cal_valence=2,
        h_valence=1.0, h_int_con=1.0, h_ext_con=1.0, h_rev_pot=-34.0,
    )
    default.update(kwargs)
    return AllProperties(**default)

class SingleComp(arbor.recipe):
    def __init__(self, props):
        super().__init__()
        self.properties = props
        self._mechs = [*self.properties.catalogue]
        self._num = len(self._mechs)

    def morphology(self):
        tree = arbor.segment_tree()
        tree.append(
            arbor.mnpos,
            arbor.mpoint(-2, 0, 0, 2),
            arbor.mpoint(2, 0, 0, 2),
            tag=1
        )
        return arbor.morphology(tree)

    def num_cells(self):
        return self._num

    def probes(self, gid):
        return [arbor.cable_probe_membrane_voltage('"midpoint"')]

    def num_sources(self, gid):
        return 0

    def cell_kind(self, gid):
        return arbor.cell_kind.cable

    def cell_description(self, gid):
        mech = self._mechs[gid]
        decor = arbor.decor()
        decor.paint('"all"', arbor.density(mech))
        return arbor.cable_cell(
            self.morphology(),
            arbor.label_dict({
                'all': '(all)',
                'midpoint': '(root)',
           }),
           decor
        )

    def global_properties(self, kind):
        return self.properties

def nrn_sim(pkg, t, dt):
    p.dt = dt
    p.celsius = 32
    time = p.time
    recorders = {}
    for mech in pkg.mods:
        s = p.Section()
        s.L = 4
        s.diam = 4
        try:
            s.insert(mech.mod_name)
        except ValueError:
            # The mod collection contains PointProcesses, skip those.
            continue
        print("inserted", mech.mod_name)
        mname = mech.asset_name
        # Match the NEURON display labels to the Arbor ones.
        if mech.variant != "0":
            mname += f"_{mech.variant}"
        if mname == "Km_granule_cell":
            mname = "Km"
        if mname == "Ca_granule_cell":
            mname = "Ca"
        recorders[mname] = p.record(s)

    p.finitialize()
    p.continuerun(t)

    return time, recorders

catalogue = glia.catalogue("dbbs")
props = make_props().properties
props.catalogue = catalogue
recipe = SingleComp(props)
context = arbor.context(threads=1, gpu_id=None)
decomp = arbor.partition_load_balance(recipe, context)
sim = arbor.simulation(recipe, decomp, context)
handles = [sim.sample((n, 0), arbor.regular_schedule(0.1), arbor.sampling_policy.exact) for n in range(recipe._num)]
tSim = 1000
dt = 0.025
sim.run(tSim, dt)
samples = [sim.samples(handle)[0][0] for handle in handles]
package = glia.package("dbbs_mod_collection")
time, mechs = nrn_sim(package, tSim, dt)
with open("single_comp.pkl", "wb") as f:
    pickle.dump(((recipe._mechs, samples), (list(time), {mech: list(trace) for mech, trace in mechs.items()})), f)
