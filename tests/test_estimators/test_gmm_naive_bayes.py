import pytest
import numpy as np

from sklego.common import flatten
from sklego.naive_bayes import GaussianMixtureNB, BayesianGaussianMixtureNB
from sklego.testing import check_shape_remains_same_classifier
from tests.conftest import nonmeta_checks, general_checks, classifier_checks, select_tests

@pytest.mark.parametrize(
    "test_fn", select_tests(
        flatten([nonmeta_checks, general_checks, classifier_checks]),
        exclude=[
            # Nonsense checks because we always need at least two columns (group and value)
            "check_fit1d",
            "check_fit2d_predict1d",
            "check_fit2d_1feature",
            "check_transformer_data_not_an_array",
            "check_methods_subset_invariance",
            "check_sample_weights_invariance",
            "check_non_transformer_estimators_n_iter"
        ],
    ),
)
def test_estimator_checks(test_fn):
    clf1 = GaussianMixtureNB()
    clf2 = GaussianMixtureNB(n_components=2)
    clf3 = BayesianGaussianMixtureNB()
    clf4 = BayesianGaussianMixtureNB(n_components=2)
    test_fn(GaussianMixtureNB.__name__, clf1)
    test_fn(GaussianMixtureNB.__name__ + "_components_5", clf2)
    test_fn(BayesianGaussianMixtureNB.__name__, clf3)
    test_fn(BayesianGaussianMixtureNB.__name__ + "_components_5", clf4)


@pytest.fixture
def dataset():
    np.random.seed(42)
    return np.concatenate([np.random.normal(0, 1, (2000, 2))])


@pytest.mark.parametrize("k", [1, 5, 10])
def test_obvious_usecase(k):
    X = np.concatenate(
        [np.random.normal(-10, 1, (100, 2)), np.random.normal(10, 1, (100, 2))]
    )
    y = np.concatenate([np.zeros(100), np.ones(100)])
    assert (GaussianMixtureNB(n_components=k).fit(X, y).predict(X) == y).all()
    assert (BayesianGaussianMixtureNB(n_components=k).fit(X, y).predict(X) == y).all()
