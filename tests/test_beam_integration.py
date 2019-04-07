from openseespy import opensees as op
import pytest


def elastic_section(section_id):

    e_conc = 30e6
    area = 0.3 * 0.4
    inertia = 0.3 * 0.4 ** 3 / 12

    op.section("Elastic", section_id, *[e_conc, area, inertia])


def bilinear_material(mat_id):
    e_conc = 30e6
    depth = 0.4
    width = 0.3
    inertia = width * depth ** 3 / 12
    ei = e_conc * inertia
    eps_yield = 300.0e6 / 200e9
    phi_y = 2.1 * eps_yield / depth
    mat_props = [ei, 0.05 * ei, phi_y]
    op.uniaxialMaterial("ElasticBilin", mat_id, *mat_props)


def uniaxial_steel01_material(mat_id):
    mat_type = 'Steel01'

    mat_args = [300e6, 200e9, 0.001]
    op.uniaxialMaterial(mat_type, mat_id, *mat_args)


def elastic_section(section_id):

    e_conc = 30e6
    area = 0.3 * 0.4
    inertia = 0.3 * 0.4 ** 3 / 12

    op.section("Elastic", section_id, *[e_conc, area, inertia])


def uniaxial_steel01_section(section_id, mat_id=None):
    if mat_id is None:
        mat_id = section_id
    uniaxial_steel01_material(mat_id)

    op.section("Uniaxial", section_id, mat_id, "Mz")


def test_define_uniaxial_steel101_section():
    op.wipe()
    op.model('basic', '-ndm', 2, '-ndf', 3)  # 2 dimensions, 3 dof per node
    section1_id = 1
    uniaxial_steel01_section(section1_id)


def test_beam_integration_mid_point_w_elastic():
    lp_i = 0.1
    lp_j = 0.2
    op.wipe()
    op.model('basic', '-ndm', 2, '-ndf', 3)  # 2 dimensions, 3 dof per node
    section_id = 1
    elastic_section(section_id)
    integ_tag = 1
    op.beamIntegration('HingeMidpoint', integ_tag, section_id, lp_i, section_id, lp_j, section_id)


#@pytest.mark.skip()
def test_beam_integration_mid_point_w_steel01():
    lp_i = 0.1
    lp_j = 0.2
    op.wipe()
    op.model('basic', '-ndm', 2, '-ndf', 3)  # 2 dimensions, 3 dof per node
    section1_id = 1
    section2_id = 2
    section3_id = 3
    uniaxial_steel01_section(section1_id)
    uniaxial_steel01_section(section2_id)
    uniaxial_steel01_section(section3_id)
    integ_tag = 1
    op.beamIntegration('HingeMidpoint', integ_tag, section1_id, lp_i, section2_id, lp_j, section3_id)
    with_force_beam_column = 1
    if with_force_beam_column:
        # Establish nodes
        bot_node = 1
        top_node = 2
        transf_tag = 1
        op.geomTransf('Linear', transf_tag, *[])
        op.node(bot_node, 0., 0.)
        op.node(top_node, 0., 5.)
        ele_i = 1
        op.element('forceBeamColumn', ele_i, bot_node, top_node, transf_tag, integ_tag)


def test_beam_integration_lobatto_w_steel01():
    op.wipe()
    op.model('basic', '-ndm', 2, '-ndf', 3)  # 2 dimensions, 3 dof per node
    section_id = 1
    uniaxial_steel01_material(section_id)
    int_tag = 1
    op.beamIntegration('Lobatto', int_tag, section_id, 8)
    assert 1 == 1  # This pass


if __name__ == '__main__':
    test_beam_integration_lobatto_w_steel01()
    test_beam_integration_mid_point_w_steel01()
