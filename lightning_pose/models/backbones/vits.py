from functools import partial
from segment_anything.modeling import ImageEncoderViT
import torch
from typeguard import typechecked


@typechecked
def build_backbone(backbone_arch: str, image_size: int = 256, **kwargs):
    """Load backbone weights for resnet models.

    Args:
        backbone_arch: which backbone version/weights to use
        image_size: height/width in pixels of images (must be square)

    Returns:
        tuple
            - backbone: pytorch model
            - mode (str): "transformer"
            - num_fc_input_features (int): number of input features to fully connected layer

    """

    mode = "transformer"

    # load backbone weights
    if "vit_h_sam" in backbone_arch:
        ckpt_url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
        state_dict = torch.hub.load_state_dict_from_url(ckpt_url)
        encoder_embed_dim = 1280
        encoder_depth = 32
        encoder_num_heads = 16
        encoder_global_attn_indexes = (7, 15, 23, 31)
        prompt_embed_dim = 256
        image_size = image_size
        vit_patch_size = 16
        base = ImageEncoderViT(
            depth=encoder_depth,
            embed_dim=encoder_embed_dim,
            img_size=image_size,
            mlp_ratio=4,
            norm_layer=partial(torch.nn.LayerNorm, eps=1e-6),
            num_heads=encoder_num_heads,
            patch_size=vit_patch_size,
            qkv_bias=True,
            use_rel_pos=True,
            global_attn_indexes=encoder_global_attn_indexes,
            window_size=14,
            out_chans=prompt_embed_dim,
        )
        base.load_state_dict(state_dict, strict=False)

    elif "vit_b_sam" in backbone_arch:
        ckpt_url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
        state_dict = torch.hub.load_state_dict_from_url(ckpt_url)
        encoder_embed_dim = 768
        encoder_depth = 12
        encoder_num_heads = 12
        encoder_global_attn_indexes = (2, 5, 8, 11)
        prompt_embed_dim = 256
        image_size = image_size
        vit_patch_size = 16
        base = ImageEncoderViT(
            depth=encoder_depth,
            embed_dim=encoder_embed_dim,
            img_size=image_size,
            mlp_ratio=4,
            norm_layer=partial(torch.nn.LayerNorm, eps=1e-6),
            num_heads=encoder_num_heads,
            patch_size=vit_patch_size,
            qkv_bias=True,
            use_rel_pos=True,
            global_attn_indexes=encoder_global_attn_indexes,
            window_size=14,
            out_chans=prompt_embed_dim,
        )
        base.load_state_dict(state_dict, strict=False)

    else:
        raise NotImplementedError

    num_fc_input_features = base.neck[-2].in_channels

    return base, mode, num_fc_input_features