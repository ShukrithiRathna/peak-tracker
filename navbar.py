import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Time-Series", href="/peaks")),
              dbc.NavItem(dbc.NavLink("Distribution", href="/app"))
              # dbc.NavItem(dbc.NavLink("Time-Series", href="/app"))
              
                    ],
          brand="Peak Tracking Application",
          brand_href="/home",
          sticky="top",
    )
    return navbar