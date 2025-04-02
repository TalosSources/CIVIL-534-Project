# Steps
* Define tunable variables (correspond to what can be changed through policy)
* Define objective variables
* Choose an algorithm
    * grid search
    * find the best one (and possibly other good choices)
* write about our methodology
* write about the findings

# Policy design
## Can be modified
* constants: through world3.init_world3_constants(...), taking many parameters
* table functions: through world3.init_world3_table_functions(...) taking a json file path
## Alternatively (not really relevant)
* delay functions: through world3.set_world3_delay_functions(...) (only taking a method name string)

## Global
* Pyear (default 1975) -> the year the policies (variables with _1, _2 variants) are applied
* iphst (default 1940) -> the year medical policies are applied? 

## Agriculture
### most interesting
* alai (average lifetime of agricultural inputs (years)) can be changed (setting alai1, alai2)
* fioaa (fraction of industrial output allocated to agriculture) works in the same way as ifpc

### other
* ifpc (indicated food per capita [vegetable-equivalent kilograms/person-year]) is a function of iopc (industrial output per capita [dollars/person-year], from the capital subsystem). There can be 2 functions (ifpc1 and ifpc2), that change at pyears
* lymap (land yield multiplier from air pollution), same 
* llmy (land life multiplier from yield)

### probably not tunable
* lyf too (land yield factor) 
* some others (falm, ... simple functional relationships)

## Capital
### Most interesting
* iopcd (industrial output per capita desired) (is not a policy (in the code), but should have a massive impact)
* alic (average lifetime of industrial capital), same
* alsc (average lifetime of service capital), same
* fioac (fraction of industrial output allocated to consumption), same
* fioas (fraction of industrial output allocated to services) same
* iet (industrial equilibrium time)

### Relationship can be changed
* cuf(lufd=labor utilization fraction delayed) (capital utilization fraction)
* jph(aiph=agricultural inputs per hectare) (jobs per hectare)
* jpscu(sopc=service output per capita) (jobs per service capital unit)
* jpicu(iopc=industrial output per capita) (jobs per industrial capital unit) -> through a simple functional relationship

### other
* icor (industrial capital-output ratio) (icor1, icor2)
* scor (service capital-output ratio), same
* fioacv (has a quite complicated relationship involving the industrial equilibrium time, not necessarily relevant)
* isopc (indicated service output per capita) -> through functional tables

## Population
### Most interesting
* hsapc(sopc=service_output_per_capita) health services allocations per capita
* fcest (fertility control effectiveness set time [year]), default is 4000, I guess it means disabled?
* fsafc(nfc=need_fertility_control) fraction of services allocated to fertility control 
* zpgt (time when desired family size equals 2 children, a bit blurry)

### other
* rlt (reproductive lifetime)
* lmf(fpc=food_per_capita/sfpc=subsistence_food_per_capita) lifetime multiplier from food

### not interesting
* ieat, lpd? are about lifetime perception delay, or income expectation averaging time
simple functional:
* m_n(le=life_expectancy) mortality rate for different population categories (not interesting)

## Resource
### Most interesting
* fcaor (fraction of capital allocated to obtaining resources) (fcaor1, fcaor2)
### Maybe not tunable
* pcrum (per capita resource usage multiplier)

## Pollution
* amti (agricultural materials toxicity index)
* imti (industrial materials toxicity index)
* imef (industrial materials emission factor)


## Initial Parameters choice
* time -> at world3 object initialization
* imti (pollution), constant
* iopcd (industrial output per capita desired) (capital) constant
* alai (average lifetime of agricultural inputs (years)): alai1 and alai2 are constants
* fsafc (population), function table, in the json (use a proportional factor for simplicity?)
* hsapc (population), function table, in the json (also a prop factor?)







