def test_plot():
    """Test that the pkanalysis file run"""
    from pkmodel.pkanalysis import plot_solution
    from pkmodel.pk_model import PKModel
    import numpy as np
    test_model = PKModel()
    test_model.create_model("central", 1)
    model_out = test_model.solve(np.linspace(0, 1, 1000), np.array([0.0]))
    plot_solution(model_out, test_model.get_compartment_names, testing=True)
    assert True
